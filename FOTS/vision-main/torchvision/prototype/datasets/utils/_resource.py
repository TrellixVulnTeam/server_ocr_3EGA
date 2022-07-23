import os.path
import pathlib
from typing import Optional, Union
from urllib.parse import urlparse

from torch.utils.data import IterDataPipe
from torch.utils.data.datapipes.iter import IterableWrapper
from torchdata.datapipes.iter import IoPathFileLoader


# FIXME
def compute_sha256(path: pathlib.Path) -> str:
    return ""


class LocalResource:
    def __init__(self, path: Union[str, pathlib.Path], *, sha256: Optional[str] = None) -> None:
        self.path = pathlib.Path(path).expanduser().resolve()
        self.file_name = self.path.name
        self.sha256 = sha256 or compute_sha256(self.path)

    def to_datapipe(self) -> IterDataPipe:
        return IoPathFileLoader(IterableWrapper((str(self.path),)), mode="rb")  # type: ignore


class OnlineResource:
    def __init__(self, url: str, *, sha256: str, file_name: str) -> None:
        self.url = url
        self.sha256 = sha256
        self.file_name = file_name

    def to_datapipe(self, root: Union[str, pathlib.Path]) -> IterDataPipe:
        path = os.path.join(root, self.file_name)
        # FIXME
        return IoPathFileLoader(IterableWrapper((str(path),)), mode="rb")  # type: ignore


# TODO: add support for mirrors
# TODO: add support for http -> https
class HttpResource(OnlineResource):
    def __init__(self, url: str, *, sha256: str, file_name: Optional[str] = None) -> None:
        if not file_name:
            file_name = os.path.basename(urlparse(url).path)
        super().__init__(url, sha256=sha256, file_name=file_name)


class GDriveResource(OnlineResource):
    def __init__(self, id: str, *, sha256: str, file_name: str) -> None:
        # TODO: can we maybe do a head request to extract the file name?
        url = f"https://drive.google.com/file/d/{id}/view"
        super().__init__(url, sha256=sha256, file_name=file_name)

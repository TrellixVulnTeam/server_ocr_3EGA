import io
from typing import cast

import PIL.Image
import torch
from torchvision.transforms.functional import pil_to_tensor

__all__ = ["raw", "pil"]


def raw(buffer: io.IOBase) -> torch.Tensor:
    raise RuntimeError("This is just a sentinel and should never be called.")


def pil(buffer: io.IOBase, mode: str = "RGB") -> torch.Tensor:
    return cast(torch.Tensor, pil_to_tensor(PIL.Image.open(buffer).convert(mode.upper())))

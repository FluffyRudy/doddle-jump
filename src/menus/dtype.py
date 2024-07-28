# -*- coding: utf-8 -*-
from typing import Protocol, Union, Optional
from pygame import Surface, Rect


class DtypeDrawable(Protocol):
    """Common drawing protocal"""

    image: Optional[Surface]
    rect: Rect
    global_x: int
    global_y: int
    parent: Union["DtypeDrawable", Surface]

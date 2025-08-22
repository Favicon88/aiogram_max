from __future__ import annotations
from typing import List, Union
from typing import Optional
from pydantic import BaseModel
from ..types import Update


class UpdatesResponse(BaseModel):
    updates: List[Union["Update", None]]
    marker: Optional[int]

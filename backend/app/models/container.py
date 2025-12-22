from pydantic import BaseModel
from datetime import datetime
from typing import Literal

TerminalName = Literal["MAHER", "APM", "PNCT"]

class Container(BaseModel):
    LFD: datetime                     # Last Free Day (date)
    container_number: str         # Text
    customer_release: bool        # Boolean
    freight_release: bool         # Boolean
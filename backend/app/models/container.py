from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Literal, Optional
from enum import Enum

class TerminalName(str, Enum):
    MAHER = "MAHER"
    APM = "APM"
    PNCT = "PNCT"

class Container(BaseModel):
    container_number: str

    available: bool = Field(
        description="True if container is available"
    )

    customs_release: bool = Field(
        description="True if customs status is RELEASED"
    )

    freight_release: bool = Field(
        description="True if freight status is RELEASED"
    )

    last_free_day: Optional[date] = Field(
        description="Last free day (may be null)"
    )     # Boolean

    terminal: TerminalName = Field(
        description="Terminal where container is located"
    )
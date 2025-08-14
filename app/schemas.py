from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class TokenData(BaseModel):
    id: Optional[int] = None
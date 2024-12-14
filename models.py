from sqlmodel import Field, SQLModel #type:ignore
from typing import Optional
from datetime import datetime

class URL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    original_url: str
    short_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    accessed_count: int = Field(default=0)

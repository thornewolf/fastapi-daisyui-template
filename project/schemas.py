from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class LogBase(BaseModel):
    content: str
    time: datetime = Field(default_factory=datetime.utcnow)


class LogCreate(LogBase):
    pass


class Log(LogBase):
    id: int

    class Config:
        orm_mode = True

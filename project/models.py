from project.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    content = Column(String(10_000), nullable=False)

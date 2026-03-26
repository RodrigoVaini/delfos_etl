from sqlalchemy import Column, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Data(Base):
    __tablename__ = "data"

    timestamp = Column(DateTime, primary_key=True)
    wind_speed = Column(Float)
    power = Column(Float)
    ambient_temperature = Column(Float)
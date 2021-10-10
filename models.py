from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AirQuality(Base):
    """
    AirQuality model
    """
    __tablename__ = "AirQuality"
    id = Column(Integer, primary_key=True, autoincrement=True)
    MeasureId = Column(Integer)
    MeasureName = Column(Text)
    MeasureType = Column(Text)
    StratificationLevel = Column(Text)
    StateFips = Column(Integer)
    StateName = Column(Text)
    CountyFips = Column(Integer)
    CountyName = Column(Text)
    ReportYear = Column(Integer)
    Value = Column(Integer)
    Unit = Column(Text)
    UnitName = Column(Text)
    DataOrigin = Column(Text)
    MonitorOnly = Column(Integer)

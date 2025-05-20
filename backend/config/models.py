from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from config.database import Database
from sqlalchemy.orm import relationship


class SpyCats(Database.Base):
    __tablename__ = "SpyCats"

    ID = Column(String, primary_key=True)
    name = Column(String)
    experience = Column(Integer)
    breed = Column(String)
    salary = Column(Integer)

    mission = relationship("Missions", back_populates="spycatRef")


class Missions(Database.Base):
    __tablename__ = "Missions"

    ID = Column(String, primary_key=True)
    cat = Column(String, ForeignKey("SpyCats.ID", ondelete="CASCADE"))
    complete = Column(Boolean)

    targets = relationship("Targets", back_populates="missionRef", passive_deletes=True)
    spycatRef = relationship("SpyCats", back_populates="mission")


class Targets(Database.Base):
    __tablename__ = "Targets"

    ID = Column(String, primary_key=True)
    mission = Column(String, ForeignKey("Missions.ID", ondelete="CASCADE"))
    name = Column(String)
    country = Column(String)
    notes = Column(String)
    complete = Column(Boolean)

    missionRef = relationship("Missions", back_populates="targets")
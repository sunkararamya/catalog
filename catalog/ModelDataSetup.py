import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()
''' declarative_base() is a factory function that constructs a
    base class for declarative class definitions'''
# creating googlemailuser table for storing gmailusers details


class GoogleMailuser(Base):
    __tablename__ = 'google_mail_user'
    r_id = Column(Integer, primary_key=True)
    r_name = Column(String(245), nullable=False)
    email = Column(String(236), nullable=False)
    picture = Column(String(224))
print('google_mail_user table is created successfully')
# creating Filmy_cameras table for storing filmcameratypes


class Filmy_Cameras(Base):
    __tablename__ = 'filmcameratype'
    r_id = Column(Integer, primary_key=True)
    r_name = Column(String(223), nullable=False)
    user_id = Column(Integer, ForeignKey('google_mail_user.r_id'))
    user = relationship(GoogleMailuser, backref="filmcameratype")

    @property
    def serialize(self):
        """ it is used to return objects of complex datatypes
        in easily serializeable formats"""
        return {
            'r_name': self.r_name,
            'r_id': self.r_id
        }
# creating Filmy_cam_Name table for differnt types of film cameras in market ..
print('filmcameratype table is created successfully')


class Filmy_cam_Name(Base):
    __tablename__ = 'filmycamname'
    r_id = Column(Integer, primary_key=True)
    r_name = Column(String(200), nullable=False)
    cam_Model = Column(String(250))
    Dimension = Column(String(160))
    Batteries = Column(String(140))
    resolution = Column(String(100))
    screen_size = Column(String(245))
    conector_type = Column(String(234))
    camera_cost = Column(String(252))
    voltage = Column(String(242))
    date = Column(DateTime, nullable=False)
    filmcameratypeid = Column(Integer, ForeignKey('filmcameratype.r_id'))
    filmcameratype = relationship(
     Filmy_Cameras, backref=backref('filmycamname', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('google_mail_user.r_id'))
    user = relationship(GoogleMailuser, backref='filmycamname')

    @property
    def serialize(self):
        """ it is used to return objects of complex datatypes
        in easily serializeable format"""
        return {
            'r_name': self. r_name,
            'cam_Model': self. cam_Model,
            'Dimension': self. Dimension,
            'Batteries': self. Batteries,
            'resolution': self. resolution,
            'screen_size': self. screen_size,
            'conector_type': self.conector_type,
            'camera_cost': self.camera_cost,
            'voltage': self.voltage,
            'date': self. date,
            'r_id': self.r_id
        }
print('filmycamname table is created successfully')
engine_1 = create_engine('sqlite:///filmcameras.db')
Base.metadata.create_all(engine_1)

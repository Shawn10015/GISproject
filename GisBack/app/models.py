from . import db
from geoalchemy2 import Geometry
import json

class City(db.Model):
    __tablename__ = 'main_table'
    adcode = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    center = db.Column(db.Float, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    geom = db.Column(Geometry('MULTYPOLYGON'))

    def to_dict(self):
        return {
            "adcode": self.adcode,
            "name": self.name,
            "center": self.center,
            "population": self.population,
            "geom": self.serialize_geom()
        }
    
    def serialize_geom(self):
        if self.geom is not None:
            return json.loads(db.session.scalar(self.geom.ST_AsGeoJSON()))
        return None

class Province(db.Model):
    __tablename__ = 'belong_table'
    adcode = db.Column(db.Integer, primary_key=True)
    province= db.Column(db.String, nullable=False)
    geom = db.Column(Geometry('MULTYPOLYGON'))

    def to_dict(self):
        return {
            "adcode": self.adcode,
            "province": self.province,
            "geom": self.serialize_geom()
        }
    
    def serialize_geom(self):
        if self.geom is not None:
            return json.loads(db.session.scalar(self.geom.ST_AsGeoJSON()))
        return None

class Scenic_spots(db.Model):
    __tablename__ = 'scenic_spots'
    id = db.Column(db.Integer, primary_key=True)
    adcode = db.Column(db.Integer, db.ForeignKey('info_table.adcode'), nullable=False)
    scenic_spots_name = db.Column(db.String, nullable=False)
    scenic_spots_level = db.Column(db.String, nullable=False)
    geom = db.Column(Geometry('POINT'))

    def to_dict(self):
        return {
            "id": self.id,
            "adcode": self.adcode,
            "scenic_spots_name": self.scenic_spots_name,
            "scenic_spots_level": self.scenic_spots_level,
            "geom": self.serialize_geom()
        }

    def serialize_geom(self):
        if self.geom is not None:
            return json.loads(db.session.scalar(self.geom.ST_AsGeoJSON()))
        return None

class Info(db.Model):
    __tablename__ = 'info_table'
    adcode = db.Column(db.Integer, primary_key=True)
    childrenNum = db.Column(db.Integer, nullable=False)
    level = db.Column(db.String, nullable=False)

    scenic_spots_data = db.relationship('Scenic_spots', backref='info', lazy=True)

    def to_dict(self):
        scenic_spots_info = []
        if self.scenic_spots_data:
            for scenic in self.scenic_spots_data:
                scenic_spots_info.append({
                    "id": scenic.id,
                    "scenic_spots_name": scenic.scenic_spots_name
                })
        
        return {
            "adcode": self.adcode,
            "childrenNum": self.childrenNum,
            "level": self.level,
            "scenic_spots_info": scenic_spots_info
        }



from extensions import db


class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'CW2'}
    UserID = db.Column(db.Integer, primary_key=True)
    Email_address = db.Column(db.String(255), unique=True, nullable=False)
    Role = db.Column(db.String(100), nullable=False)


class Trail(db.Model):
    __tablename__ = 'Trails'
    __table_args__ = {'schema': 'CW2'}
    TrailID = db.Column(db.Integer, primary_key=True)
    TrailName = db.Column(db.String(100), nullable=False)
    Difficulty = db.Column(db.String(50), nullable=False)
    Location = db.Column(db.String(100), nullable=False)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Length = db.Column(db.Float, nullable=False)
    ElevationGain = db.Column(db.Integer, nullable=False)
    TimeTaken = db.Column(db.Integer, nullable=False)







## MODEL

from app import db


class Datatype(db.Model):
    __tablename__ = "datatypes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # ONE TO MANY
    datatype = db.relationship("Network", backref="datatype", lazy="dynamic")
    # network_id = db.Column(db.Integer, db.ForeignKey("networks.id"))

    def __init__(self, name):
        self.name = name

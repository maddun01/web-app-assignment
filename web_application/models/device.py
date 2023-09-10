## MODEL

from app import db


class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    type = db.Column(db.Text)
    os = db.Column(db.Text)
    # MANY TO ONE
    ip_id = db.Column(db.Integer, db.ForeignKey("ips.id"))
    # ip = db.relationship("Ip", backref="device", uselist=False)
    date_added = db.Column(db.DateTime)
    last_run = db.Column(db.DateTime)

    def __init__(self, name, type, os, ip_id, date_added, last_run):
        self.name = name
        self.type = type
        self.os = os
        self.ip_id = ip_id
        self.date_added = date_added
        self.last_run = last_run

    def __repr__(self):
        return f"Device details: \n{self.name}\n{self.type}\n{self.os}\n{self.ip_id}\n{self.date_added}\n{self.last_run}"

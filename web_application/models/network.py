## MODEL

from app import db


class Network(db.Model):
    __tablename__ = "networks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # MANY TO ONE
    datatype_id = db.Column(db.Integer, db.ForeignKey("datatypes.id"))
    # datatype = db.relationship("Datatype", backref="network", lazy="dynamic")
    provenance = db.Column(db.Text)
    format = db.Column(db.Text)
    date_added = db.Column(db.DateTime)
    last_run = db.Column(db.DateTime)

    def __init__(self, name, datatype_id, provenance, format, date_added, last_run):
        self.name = name
        self.datatype_id = datatype_id
        self.provenance = provenance
        self.format = format
        self.date_added = date_added
        self.last_run = last_run

    def __repr__(self):
        return f"Network details: \n{self.name}\n{self.datatype_id}\n{self.provenance}\n{self.format}\n{self.date_added}\n{self.last_run}"

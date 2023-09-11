# ## MODEL

# from web_application import db


# class Ip(db.Model):
#     __tablename__ = "ips"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text)
#     # ONE TO MANY
#     device = db.relationship("Device", backref="ip", lazy="dynamic")
#     # device_id = db.Column(db.Integer, db.ForeignKey("devices.id"))

#     def __init__(self, name):
#         self.name = name

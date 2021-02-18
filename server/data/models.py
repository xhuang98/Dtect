from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserLogin(db.Model):
    __tablename__ = "userlogin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127), unique=True)
    password = db.Column(db.String(127))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Authentication(db.Model):
    __tablename__ = "authentication"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    source_user = db.Column(db.String(127))
    destination_user = db.Column(db.String(127))
    source_computer = db.Column(db.String(127))
    destination_computer = db.Column(db.String(127))
    authentication_type = db.Column(db.String(127))
    logon_type = db.Column(db.String(127))
    auth_orientation = db.Column(db.String(127))
    auth_result = db.Column(db.String(127))
    flagged = db.Column(db.Boolean(), default=None)

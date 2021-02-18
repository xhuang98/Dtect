from flask_sqlalchemy import SQLAlchemy
from api import app, db
from data.models import Authentication, UserLogin
from data.parser import authlogs
from predictions import update_predictions

# create tables
with app.app_context():
    db.create_all()

with app.app_context():
    entry = UserLogin(
        username="admin",
        password="123"
    )
    db.session.add(entry)
    db.session.commit()


# insert authentication logs
with app.app_context():
    for log in authlogs:
        entry = Authentication(
            time=log[0],
            source_user=log[1],
            destination_user=log[2],
            source_computer=log[3],
            destination_computer=log[4],
            authentication_type=log[5],
            logon_type=log[6],
            auth_orientation=log[7],
            auth_result=log[8]
        )
        db.session.add(entry)
    db.session.commit()

update_predictions(db, app.app_context())

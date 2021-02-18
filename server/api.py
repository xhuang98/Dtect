import sys
sys.path.append('../server/')

import time
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from data.models import db, Authentication, UserLogin
from predictions import update_predictions
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.DEBUG,
    event_level=logging.ERROR
)
sentry_sdk.init(
    dsn="https://de11a1016667481096a0b4fd02346103@o358880.ingest.sentry.io/5450617",
    integrations=[sentry_logging]
)

app = Flask(__name__, static_folder="./dtect-app/build", static_url_path='/')

# todo: put environment elsewhere
ENV = 'production'

if (ENV == 'production'):
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://chsmzdmeqabshc:8efa7d222d9d0cd81ab0d5bd2763080d46c885aa0063c05a68400e6635ae5205@ec2-184-72-162-198.compute-1.amazonaws.com:5432/d267i08nmjd2r7'
else:
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/dtect'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False

db.init_app(app)


# APP ROUTES

@app.route('/')
def index():
    logging.info(f"index routing")
    return app.send_static_file('index.html')


@app.route('/api/time')
def get_current_time():
    logging.info(f"get_current_time routing")
    # note: flask will automatically jsonify returned dictionary
    return {'time': time.time()}


@app.route('/login', methods=['POST'])
def handle_login():
    logging.info(f"handle_login routing")

    req_username = request.json['username']
    req_password = request.json['password']

    search_user = db.session.query(UserLogin).filter(UserLogin.username == req_username, UserLogin.password == req_password)
    if (search_user.count() != 1):
        return {"success": False, "message": "Invalid Login"}

    return {"username": req_username, "success": True}


@app.route('/logout', methods=['POST'])
def handle_logout():
    logging.info(f"handle_logout routing")
    return {"success": True}


@app.route('/authlogs', methods=['GET'])
def handle_authlogs():
    '''Returns all rows from the authentication table'''
    logging.info(f"handle_authlogs routing")
    update_predictions(db, app.app_context())

    logs = []
    for log in db.session.query(Authentication).all():
        serialized = log.__dict__
        serialized.pop('_sa_instance_state')
        logs.append(log.__dict__)

    return {"success": True, "logs": logs}

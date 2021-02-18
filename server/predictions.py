from data.models import Authentication
from data_analysis import *
from data_analysis.los_alamos_processing import *
from data_analysis.predict import evaluate
from data_analysis import data_config
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


def calculate_prediction(db, entry: Authentication):
    """
    Given an authentication entry from the database, return model prediction.
    """
    logging.info(f"Predicting for entry {entry.id}")
    query = db.session.query(Authentication).filter_by(source_user=entry.source_user).order_by(Authentication.time)
    history = [event for event in query if int(event.time) < int(entry.time)]
    if len(history) == 0:
        return False
    while len(history) < data_config.window_size:
        history.append(history[-1])
    try:
        return evaluate([{
                'timestamp': event.time,
                'src_user': event.source_user,
                'dest_user': event.destination_user,
                'src_comp': event.source_computer,
                'dest_comp': event.destination_computer,
                'auth_type': event.authentication_type,
                'logon_type': event.logon_type,
                'auth_orientation': event.auth_orientation == 'LogOn',
                'success': event.auth_result == 'Success'
            } for event in history[:data_config.window_size]])
    except ValueError:
        return None


def update_predictions(db, context):
    """
    Go through entries in the authentication database and update prediction values.
    """
    #with app.app_context():
    with context:
        logging.info(f"Prediction update initiated...")
        query = db.session.query(Authentication).filter(Authentication.flagged == None).all()
        for event in query:
            prediction = calculate_prediction(db, event)
            event.flagged = prediction
            db.session.commit()
        logging.info(f"Prediction update complete")


if __name__ == '__main__':
    from api import app, db
    update_predictions(db, app.app_context())

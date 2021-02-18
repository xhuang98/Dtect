import json
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


def parse_line(line):
    """
    Parse a line in the auth event dataset.
    
    This data represents authentication events collected from individual Windows-based desktop computers, 
    servers, and Active Directory servers. Each event is on a separate line in the form of "time,
    source user@domain,destination user@domain,source computer,destination computer,authentication type,
    logon type,authentication orientation,success/failure" and represents an authentication event at the
    given time. The values are comma delimited and any fields that do not have a valid value are represented 
    as a question mark ('?').
    Example: 244,C1$@DOM1,C1$@DOM1,C1,C529,Kerberos,Network,LogOn,Success
    """
    fields = line.split(',')
    assert len(fields) == 9
    
    return {
        "timestamp": fields[0],
        "src_user": fields[1],
        "dest_user": fields[2],
        "src_comp": fields[3],
        "dest_comp": fields[4],
        "auth_type": fields[5],
        "logon_type": fields[6],
        "auth_orientation": fields[7] == 'LogOn',
        "success": fields[8] == 'Success'
    }


def load_mapping(filename):
    """
    Load mapping dict from file.

    :param filename: mapping file name
    :return: dictionary of key to one-hot encoding; number of keys
    """
    f = open(filename)
    mapping = json.load(f)
    return mapping, len(mapping)


def calculate_input_vector_length(user_count, computer_count, auth_type_count, logon_type_count):
    """
    Return model input vector length with user, computer, auth_type, logon_type one-hot encoded.
    """
    return 3 + 2 * user_count + 2 * computer_count + auth_type_count + logon_type_count

import sys
import numpy as np
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from data_analysis.model import *
from data_analysis.dataset import construct_encoding
from data_analysis.los_alamos_processing.util import load_mapping, calculate_input_vector_length
from data_analysis import data_config
sys.path.append('./data_analysis/')

sentry_logging = LoggingIntegration(
    level=logging.DEBUG,
    event_level=logging.ERROR
)
sentry_sdk.init(
    dsn="https://de11a1016667481096a0b4fd02346103@o358880.ingest.sentry.io/5450617",
    integrations=[sentry_logging]
)


def load_model(input_size):
    """
    Load model from presaved weights (path indicated in config file).
    :param input_size: model input channel size
    :return: model
    """
    logging.info(f"Loading model from {data_config.state_dict_path}")
    model = AutoEncoder(input_size)
    model.load_state_dict(torch.load(data_config.state_dict_path, map_location=torch.device('cpu')))
    return model


def evaluate(window, threshold=30):
    """
    Process input and perform model evaluation.

    :param window: list of dicts as input window of desired size;
    each dict should include the following strings as key:
    timestamp, src_user, dest_user, src_comp, dest_comp, auth_type, logon_type, auth_orientation, success
    :param threshold: prediction loss threshold for outlier detection
    :return: boolean (True if outlier)
    """
    if len(window) != data_config.window_size:
        error = f"Window length expected to be {data_config.window_size}, actual length {len(window)}."
        logging.error(error)
        raise ValueError(error)

    user_map, user_count = load_mapping(data_config.user_map_path)
    computer_map, computer_count = load_mapping(data_config.computer_map_path)
    auth_type_map, auth_type_count = load_mapping(data_config.auth_type_map_path)
    logon_type_map, logon_type_count = load_mapping(data_config.logon_type_map_path)

    input_size = calculate_input_vector_length(user_count, computer_count, auth_type_count, logon_type_count)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = load_model(input_size).to(device)
    model.eval()
    criterion = torch.nn.MSELoss()

    try:
        encodings = [
            construct_encoding(
                event, user_count, computer_count, auth_type_count, logon_type_count,
                user_map, computer_map, auth_type_map, logon_type_map
            )
            for event in window
        ]
    except KeyError:
        error = "Incomplete dict(s) in window"
        logging.error(error)
        raise ValueError(error)

    input_numpy = np.concatenate(encodings, axis=0).astype(np.float)
    input_tensor = torch.from_numpy(input_numpy).to(device)
    output = model(input_tensor.float()).double()
    train_loss = criterion(output, input_tensor).item()

    return train_loss > threshold

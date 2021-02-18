import os
import random
import numpy as np
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from data_analysis.los_alamos_processing import util

random.seed(10)

sentry_logging = LoggingIntegration(
    level=logging.DEBUG,
    event_level=logging.ERROR
)
sentry_sdk.init(
    dsn="https://de11a1016667481096a0b4fd02346103@o358880.ingest.sentry.io/5450617",
    integrations=[sentry_logging],
    traces_sample_rate=1.0
)



class Dataset:
    def __init__(self, dir_path, window_size,
                 user_map_path, computer_map_path, auth_type_map_path, logon_type_map_path):
        """
        Iterable dataset class for parsing los alamos data.

        :param dir_path: directory path of the txt files
        :param window_size: window size for prediction
        :param user_map_path: path to user one hot mapping
        :param computer_map_path: path to computer one hot mapping
        :param auth_type_map_path: path to auth type one hot mapping
        :param logon_type_map_path: path to logon one hot mapping
        """
        logging.info(f"Initiating Dataset instance for directory {dir_path}")
        self.directory = dir_path
        self.filenames = [filename for filename in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, filename))]
        assert len(self.filenames) > 0
        random.shuffle(self.filenames)
        self.window_size = window_size
        self.len = self.count_len()
        self.user_map, self.user_count = util.load_mapping(user_map_path)
        self.computer_map, self.computer_count = util.load_mapping(computer_map_path)
        self.auth_type_map, self.auth_type_count = util.load_mapping(auth_type_map_path)
        self.logon_type_map, self.logon_type_count = util.load_mapping(logon_type_map_path)

    def __iter__(self):
        self.file_idx = 0
        self.file_offset = 0
        self.line_count = 0
        return self

    def count_len(self):
        """
        Count total number of valid windows among all files in the data directory.

        :return: total window number
        """
        total = 0
        for filename in self.filenames:
            f = open(os.path.join(self.directory, filename))
            line_count = 0
            for _ in f:
                line_count += 1
            if line_count < self.window_size:
                continue
            else:
                total += line_count - self.window_size + 1
        return total

    def construct_encoding(self, values):
        """
        Encode input string values and construct input vector for the model.

        :param values: dictionary of input values
        :return: numpy vector
        """
        return construct_encoding(
            values, self.user_count, self.computer_count, self.auth_type_count, self.logon_type_count,
            self.user_map, self.computer_map, self.auth_type_map, self.logon_type_map)
    
    def __len__(self):
        return self.len

    def __next__(self):
        """
        Within a file, locate and return next valid window.
        If no more valid windows can be constructed, move to next data file and construct window.

        :return: 2d numpy vector; Size: window_size x encoding_size
        """
        window = []
        file_obj = open(os.path.join(self.directory, self.filenames[self.file_idx]))
        file_obj.seek(self.file_offset, 0)
        while len(window) < self.window_size:
            line = file_obj.readline()
            if line:
                if not window:
                    # Offset first line for next window parse
                    self.file_offset += len(line) + 1
                    self.line_count += 1
                try:
                    values = util.parse_line(line)
                    window.append(self.construct_encoding(values))
                except AssertionError:
                    logging.error(f"Invalid line: {line}")
                    continue
            else:
                if self.file_idx == len(self.filenames) - 1:
                    raise StopIteration 
                    
                # Restart window with new file
                window = []
                self.file_idx += 1
                self.file_offset = 0
                self.line_count = 0
                file_obj.close()
                file_obj = open(os.path.join(self.directory, self.filenames[self.file_idx]))

        file_obj.close()
        return np.concatenate(window, axis=0).astype(np.float)

    def get_encoding_len(self):
        return util.calculate_input_vector_length(self.user_count, self.computer_count,
                                                  self.auth_type_count, self.logon_type_count)


def construct_encoding(values,
                       user_count, computer_count, auth_type_count, logon_type_count,
                       user_map, computer_map, auth_type_map, logon_type_map):
    """
    Encode input string values and construct input vector for the model.

    :param values: dict of value names to string values
    :param user_count: number of users
    :param computer_count: number of computers
    :param auth_type_count: number of authentication types
    :param logon_type_count: number of logon types
    :param user_map: mapping from user name to one-hot encoding index
    :param computer_map: mapping from computer name to one-hot encoding index
    :param auth_type_map: mapping from authentication type name to one-hot encoding index
    :param logon_type_map: mapping from logon type name to one-hot encoding index
    :return: numpy vector
    """
    logging.info(f"Constructing encoding from the following event values: {values}")
    src_user_vec = np.zeros(user_count)
    dest_user_vec = np.zeros(user_count)
    src_user_vec[user_map.get(values['src_user'], user_map.get('?', 0))] = 1
    dest_user_vec[user_map.get(values['dest_user'], user_map.get('?', 0))] = 1

    src_computer_vec = np.zeros(computer_count)
    dest_computer_vec = np.zeros(computer_count)
    src_computer_vec[computer_map.get(values['src_comp'], computer_map.get('?', 0))] = 1
    dest_computer_vec[computer_map.get(values['dest_comp'], computer_map.get('?', 0))] = 1

    auth_type_vec = np.zeros(auth_type_count)
    auth_type_vec[auth_type_map.get(values['auth_type'], auth_type_map.get('?', 0))] = 1

    logon_type_vec = np.zeros(logon_type_count)
    logon_type_vec[logon_type_map.get(values['logon_type'], logon_type_map.get('?', 0))] = 1

    timestamp_vec = np.array([int(values['timestamp'])])
    auth_orientation_vec = np.array([int(values['auth_orientation'])])
    success_vec = np.array([int(values['success'])])

    return np.concatenate([
        timestamp_vec,
        src_user_vec, dest_user_vec,
        src_computer_vec, dest_computer_vec,
        auth_type_vec, logon_type_vec,
        auth_orientation_vec, success_vec
    ], axis=None).reshape((1, -1))

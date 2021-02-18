import sys
import numpy as np
sys.path.append('../../server/data_analysis/')
sys.path.append('../../server/')
from dataset import *


def test_construct_encoding():
    values = {
        'src_user': 'A123',
        'dest_user': 'A321',
        'src_comp': 'B123',
        'dest_comp': 'B321',
        'auth_type': 'ABC',
        'logon_type': 'ABC',
        'timestamp': '123',
        'auth_orientation': True,
        'success': False
    }
    user_map = {'?': 0, 'A123': 1, 'A321': 2}
    computer_map = {'?': 0, 'B123': 1, 'B321': 2}
    auth_type_map = {'?': 0, 'ABC': 1}
    logon_type_map = {'?': 0, 'ABC': 1}
    user_count, computer_count, auth_type_count, logon_type_count = 3, 3, 2, 2
    encoding = \
        construct_encoding(values,
                           user_count, computer_count, auth_type_count, logon_type_count,
                           user_map, computer_map, auth_type_map, logon_type_map)
    assert np.array_equal(encoding, np.array([[123, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0]]))


def test_dataset_len():
    dataset = Dataset(dir_path="test_dataset", window_size=5,
                      user_map_path="mock_user_map.json", computer_map_path="mock_computer_map.json",
                      auth_type_map_path="mock_auth_type_map.json",
                      logon_type_map_path="mock_logon_type_map.json")
    assert len(dataset) == 4
    assert dataset.get_encoding_len() == 15

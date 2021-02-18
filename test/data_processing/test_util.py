import sys
sys.path.append('../../server/data_analysis/los_alamos_processing/')
from util import *


def test_parse_line():
    line = "244,C1$@DOM1,C1$@DOM1,C1,C529,Kerberos,Network,LogOn,Success"
    values = parse_line(line)
    expected = {
        "timestamp": "244",
        "src_user": "C1$@DOM1",
        "dest_user": "C1$@DOM1",
        "src_comp": "C1",
        "dest_comp": "C529",
        "auth_type": "Kerberos",
        "logon_type": "Network",
        "auth_orientation": True,
        "success": True
    }
    assert values == expected


def test_load_mapping():
    file = "mock_user_map.json"
    mapping, count = load_mapping(file)
    expected = {"key1": 1, "key2": 2}
    assert mapping == expected
    assert count == 2


def test_calculate_input_vector_length():
    user_count, computer_count, auth_type_count, logon_type_count = 1, 2, 3, 4
    assert calculate_input_vector_length(user_count, computer_count, auth_type_count, logon_type_count) == 16

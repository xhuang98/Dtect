import sys
import numpy as np
sys.path.append('../../server/data_analysis/')
from predict import *


def test_evaluate():
    window = [{
            'timestamp': '123',
            'src_user': 'C1$@DOM1',
            'dest_user': 'C1$@DOM1',
            'src_comp': 'C1',
            'dest_comp': 'C1',
            'auth_type': 'Kerberos',
            'logon_type': 'Network',
            'auth_orientation': False,
            'success': False
        }] * 5
    prediction = evaluate(window)
    assert isinstance(prediction, bool)

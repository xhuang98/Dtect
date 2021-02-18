# Data Analysis

We are using an auto-encoder [model](./model.py) trained on a subset of the authentication data from the 
["*Comprehensive, Multi-Source Cyber-Security Events*"](https://csr.lanl.gov/data/cyber1/)
dataset by Los Alamos National Lab.


## Usage

### Data processing
Data processing scripts are located in [`los_alamos_processing/`](los_alamos_processing/).

- [`parse_auth.py`](los_alamos_processing/parse_auth.py) for parsing the `auth.txt` file (downloaded from the Los Alamos dataset's website).
This script sorts events by source user saved in separate files.
- [`create_one_hot_dict.py`](los_alamos_processing/create_one_hot_dict.py) for indexing source users, destination users, sources computers, destination computers,
authentication types, and logon types for one-hot vector construction. Mappings are saved as json files.
- [`data_split.py`](los_alamos_processing/data_split.py) for splitting files randomly into training, validation, and test sets.

### Prediction

[`predict.py`](predict.py):
- `load_model()` for loading model. Saved weights can be found in `checkpoints/`.
- `evaluate()` for outlier prediction. Input window must match requirements from the docstrings.
  - **Note:** `threshold` is a hyper-parameter to be tuned for accuracy

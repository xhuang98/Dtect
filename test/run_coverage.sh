#!/usr/bin/env bash

export CC_TEST_REPORTER_ID=0dc65c4be8f5469c1afcc946784038e4fd50b2ad626a15fab135c7ac1c3e3df9
./cc-test-reporter before-build

coverage run -m pytest ./test_suites.py
coverage report --include="*Dtect*" && coverage json --include="*Dtect*" && coverage xml --include="*Dtect*"
./cc-test-reporter format-coverage -t coverage.py coverage.xml

cd data_processing/
coverage run -m pytest .
coverage report --include="*Dtect*" && coverage json --include="*Dtect*" && coverage xml --include="*Dtect*"
../cc-test-reporter format-coverage -t coverage.py coverage.xml

cd ..
./cc-test-reporter sum-coverage coverage/codeclimate.json data_processing/coverage/codeclimate.json
python3 fix_name.py

./cc-test-reporter upload-coverage

#!/bin/bash

./clean.sh
#python3 setup.py sdist bdist_wheel
python3 setup.py sdist || exit 1
twine upload dist/*.tar.gz || exit 1
./clean.sh

#! /bin/bash

I='(install dependencies): '

echo "$I Pip upgrade"
python -m pip install --upgrade pip
echo "$I Installing dependencies"
python -m pip install -r ../requirements.txt
echo "Dependency Installed [OK]"

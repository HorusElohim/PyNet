#! /bin/bash

source source.sh

I='(test): '
echo "$I Testing ..."
python -m pytest
echo "$I Test Completed."


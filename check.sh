#! /bin/bash

source source.sh

flake8 --config setup.cfg src

mypy src



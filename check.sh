#! /bin/bash

source source.sh

flake8 --ignore=F403 src

mypy src



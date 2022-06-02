#! /bin/bash

I='(create_env): '

py=$1

echo "$I Creating python environment with: $py"
$py -m venv ../venv
echo "$I Environment created."



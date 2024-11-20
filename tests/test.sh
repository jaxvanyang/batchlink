#!/usr/bin/env bash
#
# Simple sanity check

set -e

export PYTHONPATH="$PWD/src"

mkdir -p test && cd test
mkdir -p a b && rm -rf a/* b/*
touch a/0.log a/1.log a/1.txt a/2.txt

# Dry run all mode combinations
python3 -m batchlink -S a -d b --dry-run '*' '{path}'
python3 -m batchlink -S a -d b -c --dry-run '*' '{path}'
python3 -m batchlink -S a -d b -R --dry-run '*' '{path}'
python3 -m batchlink -S a -d b -sR --dry-run '*' '{path}'
python3 -m batchlink -S a -d b -r --dry-run '*' '{path}'

# Same as above, but with different input & output
python3 -m batchlink -S a -d b --dry-run '*.log' '{num}.log'
python3 -m batchlink -S a -d b -c --dry-run '*.log' '{num}.log'
python3 -m batchlink -S a -d b -R --dry-run '*.log' '{num}.log'
python3 -m batchlink -S a -d b -sR --dry-run '*.log' '{num}.log'
python3 -m batchlink -S a -d b -r --dry-run '*.log' '{num}.log'

# Real run all mode combinations
python3 -m batchlink -S a -d b -f '*' '{path}'
python3 -m batchlink -S a -d b -c -f '*' '{path}'
python3 -m batchlink -S a -d b -R -f '*' '{path}'
python3 -m batchlink -S a -d b -sR -f '*' '{path}'
python3 -m batchlink -S a -d b -r -f '*' '{path}'

# Same as above, but with different input & output
python3 -m batchlink -S a -d b -f '*.log' '{num}.log'
python3 -m batchlink -S a -d b -c -f '*.log' '{num}.log'
python3 -m batchlink -S a -d b -R -f '*.log' '{num}.log'
python3 -m batchlink -S a -d b -sR -f '*.log' '{num}.log'
python3 -m batchlink -S a -d b -r -f '*.log' '{num}.log'

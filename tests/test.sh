#!/usr/bin/env bash
# use rere.py, see https://github.com/tsoding/rere.py
rm -rf a b && mkdir -p a b
touch a/0.log a/1.log a/1.txt a/2.txt
pdm run batchlink -S a -d b --dry-run '*' '{path}'
pdm run batchlink -S a -d b -c --dry-run '*' '{path}'
pdm run batchlink -S a -d b -R --dry-run '*' '{path}'
pdm run batchlink -S a -d b -sR --dry-run '*' '{path}'
pdm run batchlink -S a -d b --dry-run '*.log' '{num}.log'
pdm run batchlink -S a -d b -c --dry-run '*.log' '{num}.log'
pdm run batchlink -S a -d b -R --dry-run '*.log' '{num}.log'
pdm run batchlink -S a -d b -sR --dry-run '*.log' '{num}.log'
pdm run batchlink -S a -d b -f '*' '{path}'
pdm run batchlink -S a -d b -c -f '*' '{path}'
pdm run batchlink -S a -d b -R -f '*' '{path}'
pdm run batchlink -S a -d b -sR -f '*' '{path}'
pdm run batchlink -S a -d b -f '*.log' '{num}.log'
pdm run batchlink -S a -d b -c -f '*.log' '{num}.log'
pdm run batchlink -S a -d b -R -f '*.log' '{num}.log'
pdm run batchlink -S a -d b -sR -f '*.log' '{num}.log'
pdm run batchlink -S a -d b -r --dry-run '*' '{path}'
pdm run batchlink -S a -d b -r --dry-run '*.log' '{num}.log'
pdm run batchlink -S a -d b -r -f '*.log' '{num}.log'
pdm run batchlink -S a -d b -r -f '*' '{path}'

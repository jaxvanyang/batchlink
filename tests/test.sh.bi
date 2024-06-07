:i count 24
:b shell 19
#!/usr/bin/env bash
:i returncode 0
:b stdout 0

:b stderr 0

:b shell 53
# use rere.py, see https://github.com/tsoding/rere.py
:i returncode 0
:b stdout 0

:b stderr 0

:b shell 26
rm -rf a b && mkdir -p a b
:i returncode 0
:b stdout 0

:b stderr 0

:b shell 37
touch a/0.log a/1.log a/1.txt a/2.txt
:i returncode 0
:b stdout 0

:b stderr 0

:b shell 50
pdm run batchlink -S a -d b --dry-run '*' '{path}'
:i returncode 0
:b stdout 144
Create hard link b/0.log to a/0.log
Create hard link b/1.log to a/1.log
Create hard link b/1.txt to a/1.txt
Create hard link b/2.txt to a/2.txt

:b stderr 0

:b shell 53
pdm run batchlink -S a -d b -c --dry-run '*' '{path}'
:i returncode 0
:b stdout 96
Copy a/0.log to b/0.log
Copy a/1.log to b/1.log
Copy a/1.txt to b/1.txt
Copy a/2.txt to b/2.txt

:b stderr 0

:b shell 53
pdm run batchlink -S a -d b -R --dry-run '*' '{path}'
:i returncode 0
:b stdout 144
Create hard link b/0.log to a/0.log
Create hard link b/1.log to a/1.log
Create hard link b/1.txt to a/1.txt
Create hard link b/2.txt to a/2.txt

:b stderr 0

:b shell 54
pdm run batchlink -S a -d b -sR --dry-run '*' '{path}'
:i returncode 0
:b stdout 172
Create symbolic link b/0.log to ../a/0.log
Create symbolic link b/1.log to ../a/1.log
Create symbolic link b/1.txt to ../a/1.txt
Create symbolic link b/2.txt to ../a/2.txt

:b stderr 0

:b shell 57
pdm run batchlink -S a -d b --dry-run '*.log' '{num}.log'
:i returncode 0
:b stdout 72
Create hard link b/1.log to a/0.log
Create hard link b/2.log to a/1.log

:b stderr 0

:b shell 60
pdm run batchlink -S a -d b -c --dry-run '*.log' '{num}.log'
:i returncode 0
:b stdout 48
Copy a/0.log to b/1.log
Copy a/1.log to b/2.log

:b stderr 0

:b shell 60
pdm run batchlink -S a -d b -R --dry-run '*.log' '{num}.log'
:i returncode 0
:b stdout 72
Create hard link b/1.log to a/0.log
Create hard link b/2.log to a/1.log

:b stderr 0

:b shell 61
pdm run batchlink -S a -d b -sR --dry-run '*.log' '{num}.log'
:i returncode 0
:b stdout 86
Create symbolic link b/1.log to ../a/0.log
Create symbolic link b/2.log to ../a/1.log

:b stderr 0

:b shell 43
pdm run batchlink -S a -d b -f '*' '{path}'
:i returncode 0
:b stdout 144
Create hard link b/0.log to a/0.log
Create hard link b/1.log to a/1.log
Create hard link b/1.txt to a/1.txt
Create hard link b/2.txt to a/2.txt

:b stderr 0

:b shell 46
pdm run batchlink -S a -d b -c -f '*' '{path}'
:i returncode 0
:b stdout 156
Remove b/0.log
Copy a/0.log to b/0.log
Remove b/1.log
Copy a/1.log to b/1.log
Remove b/1.txt
Copy a/1.txt to b/1.txt
Remove b/2.txt
Copy a/2.txt to b/2.txt

:b stderr 0

:b shell 46
pdm run batchlink -S a -d b -R -f '*' '{path}'
:i returncode 0
:b stdout 204
Remove b/0.log
Create hard link b/0.log to a/0.log
Remove b/1.log
Create hard link b/1.log to a/1.log
Remove b/1.txt
Create hard link b/1.txt to a/1.txt
Remove b/2.txt
Create hard link b/2.txt to a/2.txt

:b stderr 0

:b shell 47
pdm run batchlink -S a -d b -sR -f '*' '{path}'
:i returncode 0
:b stdout 232
Remove b/0.log
Create symbolic link b/0.log to ../a/0.log
Remove b/1.log
Create symbolic link b/1.log to ../a/1.log
Remove b/1.txt
Create symbolic link b/1.txt to ../a/1.txt
Remove b/2.txt
Create symbolic link b/2.txt to ../a/2.txt

:b stderr 0

:b shell 50
pdm run batchlink -S a -d b -f '*.log' '{num}.log'
:i returncode 0
:b stdout 87
Remove b/1.log
Create hard link b/1.log to a/0.log
Create hard link b/2.log to a/1.log

:b stderr 0

:b shell 53
pdm run batchlink -S a -d b -c -f '*.log' '{num}.log'
:i returncode 0
:b stdout 78
Remove b/1.log
Copy a/0.log to b/1.log
Remove b/2.log
Copy a/1.log to b/2.log

:b stderr 0

:b shell 53
pdm run batchlink -S a -d b -R -f '*.log' '{num}.log'
:i returncode 0
:b stdout 102
Remove b/1.log
Create hard link b/1.log to a/0.log
Remove b/2.log
Create hard link b/2.log to a/1.log

:b stderr 0

:b shell 54
pdm run batchlink -S a -d b -sR -f '*.log' '{num}.log'
:i returncode 0
:b stdout 116
Remove b/1.log
Create symbolic link b/1.log to ../a/0.log
Remove b/2.log
Create symbolic link b/2.log to ../a/1.log

:b stderr 0

:b shell 53
pdm run batchlink -S a -d b -r --dry-run '*' '{path}'
:i returncode 0
:b stdout 104
Rename a/0.log to b/0.log
Rename a/1.log to b/1.log
Rename a/1.txt to b/1.txt
Rename a/2.txt to b/2.txt

:b stderr 0

:b shell 60
pdm run batchlink -S a -d b -r --dry-run '*.log' '{num}.log'
:i returncode 0
:b stdout 52
Rename a/0.log to b/1.log
Rename a/1.log to b/2.log

:b stderr 0

:b shell 53
pdm run batchlink -S a -d b -r -f '*.log' '{num}.log'
:i returncode 0
:b stdout 82
Remove b/1.log
Rename a/0.log to b/1.log
Remove b/2.log
Rename a/1.log to b/2.log

:b stderr 0

:b shell 46
pdm run batchlink -S a -d b -r -f '*' '{path}'
:i returncode 0
:b stdout 82
Remove b/1.txt
Rename a/1.txt to b/1.txt
Remove b/2.txt
Rename a/2.txt to b/2.txt

:b stderr 0


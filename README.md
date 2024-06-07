# batchlink

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Flake8: checked](https://img.shields.io/badge/flake8-checked-blueviolet)](https://flake8.pycqa.org)

[![Packaging status](https://repology.org/badge/vertical-allrepos/python:batchlink.svg)](https://repology.org/project/python:batchlink/versions)

Batch link files without modifying original files.

## Why

To solve the problem - [Is there a way to rename files from a torrent and still be able to seed?](https://www.reddit.com/r/qBittorrent/comments/ie3p10/is_there_a_way_to_rename_files_from_a_torrent_and)
If you are serving BT files on a media server like [Jellyfin](https://jellyfin.org), you
may want this.

## Features

- A CLI to easily batch link, rename, copy files.
- An extensible library.

## Examples

Create example files:

```bash
mkdir -p a b && touch a/0.log a/1.log a/1.txt a/2.txt
```

Create hard links in `b/` pointing to all files in `a/` with original file names:

> [!NOTE]
> It's recommended to add option `--dry-run` to see what will happen at first.

```console
$ batchlink -S a -d b '*' '{path}'
Create hard link b/0.log to a/0.log
Create hard link b/1.log to a/1.log
Create hard link b/1.txt to a/1.txt
Create hard link b/2.txt to a/2.txt
```

Only create links for log files:

```console
$ batchlink -S a -d b '*.log' '{path}'
Create hard link b/0.log to a/0.log
Create hard link b/1.log to a/1.log
```

And rename to one-based numbering file names:

```console
$ batchlink -S a -d b '*.log' '{num}.log'
Create hard link b/1.log to a/0.log
Create hard link b/2.log to a/1.log
```

Format replacement values:

```console
$ batchlink -S a -d b '*.log' '{num:02}.log'
Create hard link b/01.log to a/0.log
Create hard link b/02.log to a/1.log
```

Absolute symbolic link, relative symbolic link, rename, copy:

```bash
batchlink -s -S a -d b '*.log' '{num:02}.log'
batchlink -sR -S a -d b '*.log' '{num:02}.log'
batchlink -r -S a -d b '*.log' '{num:02}.log'
batchlink -c -S a -d b '*.log' '{num:02}.log'
```

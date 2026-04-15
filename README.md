# gitclone-org

Download all public repositories from a GitHub organization with optional filtering.

## Features

- Download all repos from a GitHub org
- Filter by:
  - `all` (default)
  - `original` (non-forked)
  - `forked`
- Simple and fast cloning using Git

## Requirements

- Python 3
- Git installed
- Python package:


## Usage

```bash
python downloader.py <org_url> [--type all|original|forked] [--output folder]

python downloader.py https://github.com/orgs/teslamotors/repositories

python downloader.py https://github.com/orgs/teslamotors/repositories --type original

python downloader.py https://github.com/orgs/teslamotors/repositories --type forked

python downloader.py https://github.com/orgs/teslamotors/repositories --output my_repos


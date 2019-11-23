#!/usr/bin/env python

from pathlib import Path
from sys import stderr
import requests
import yaml

MANIFEST_PATH = Path('data', 'data_manifest.yaml')
DATA_DIR = Path('data')

def read_manifest():
    """
    returns list of tuples, with file filepath and source url
    """
    mani = yaml.load(MANIFEST_PATH.open(), Loader=yaml.BaseLoader)
    return [(filepath, v['url']) for filepath, v in mani.items()]


def fetch_file(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        # be noisy and alert the user that the download unexpectedly failed
        raise ValueError(f"Got status code {resp.status_code} for: {url}")
    return resp.content


def main():
    for relpath, url in read_manifest():
        stderr.write("\n")
        stderr.write(f"Downloading: {url}\n")
        content = fetch_file(url)
        # relpath is something like stashed/originals/2010.xls
        # but we want data/stashed/originals/2010.xls
        dest_path = DATA_DIR.joinpath(relpath)
        dest_path.parent.mkdir(exist_ok=True, parents=True)

        stderr.write(f"\tWriting {len(content)} bytes to: {dest_path}\n")
        dest_path.write_bytes(content)

if __name__ == '__main__':
    main()

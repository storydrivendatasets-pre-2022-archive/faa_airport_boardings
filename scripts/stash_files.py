#!/usr/bin/env python

"""
stash_files.py

Gets all original files, as enumerated in data_manifest.yaml

"""


from pathlib import Path
from sys import stderr
import requests
import yaml

INVENTORY_PATH = Path('data_inventory.yaml')

def read_inventory():
    """
    returns list of tuples, with file filepath and source url
    """
    mani = yaml.load(INVENTORY_PATH.open(), Loader=yaml.BaseLoader)
    return [(filepath, v['url']) for filepath, v in mani.items()]


def fetch_file(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        # be noisy and alert the user that the download unexpectedly failed
        raise ValueError(f"Got status code {resp.status_code} for: {url}")
    return resp.content


def main():
    for filename, url in read_inventory():
        if 'stashed/' in filename:
            stderr.write("\n")
            stderr.write(f"Downloading: {url}\n")
            content = fetch_file(url)

            dest_path = Path(filename)
            dest_path.parent.mkdir(exist_ok=True, parents=True)

            stderr.write(f"\tWriting {len(content)} bytes to: {dest_path}\n")
            dest_path.write_bytes(content)

if __name__ == '__main__':
    main()

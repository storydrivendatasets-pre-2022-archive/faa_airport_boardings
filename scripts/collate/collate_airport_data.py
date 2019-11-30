#!/usr/bin/env python

"""
collate_airport_datapy

gather CSV files from data/converted/airport_data
write to data/collated/*.csv

$ scripts/collate/collate_airport_data.py
"""
import csv
import json
from pathlib import Path
import re
from sys import stderr

SRC_DIR = Path('data', 'converted', 'airport_data')
DEST_DIR= Path('data', 'collated',)



def cleantext(text):
    # for some reason, the FAA funky xls data had quote marks prepended `'` in certain columns
    if text and text[0] == "'" and "'" not in text[1:]:
        txt = text[1:]
    else:
        txt = text
    return re.sub(r'\s{2,}', ' ', txt).strip()


def camel_to_snake(txt):
    """given camel-case, returns a snake-cased string; via: https://stackoverflow.com/a/1176023/160863"""
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', txt.strip())
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()

def process_file(srcpath):
    """
    Returns a tuple: (headers, data)
        headers is a list of strings
        data is a list of lists

    """
    with open(srcpath) as src:
        records = list(csv.reader(src))

    headers = [camel_to_snake(h) for h in records[0]]
    data = [[cleantext(v) for v in row] for row in records[1:]]
    return (headers, data)



def main():
    DEST_DIR.mkdir(exist_ok=True, parents=True)
    for srcpath in SRC_DIR.glob('*.csv'):
        stderr.write(f"Opening {srcpath}\n")
        headers, data = process_file(srcpath)


        destpath = DEST_DIR.joinpath(srcpath.name)
        stderr.write(f"Writing {len(data)} rows to {destpath}\n")
        with open(destpath, 'w') as destfile:
            outs = csv.writer(destfile)
            outs.writerow(headers)
            outs.writerows(data)

if __name__ == '__main__':
    main()

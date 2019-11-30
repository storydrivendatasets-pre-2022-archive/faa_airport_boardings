#!/usr/bin/env python

"""
collate.py

gather files from data/stashed/processed.csv

- Remove ,$ from salary column
- collapse and strip whitespace
- unite them as data/collated/airport_annual_boardings.csv
"""
import csv
import json
from pathlib import Path
import re
from sys import stderr

SRC_DIR = Path('data', 'converted', 'boardings')
DEST_PATH = Path('data', 'collated', 'boardings.csv')


OUTPUT_HEADERS = ('year', 'rank', 'region', 'state',
                  'airport_code', 'airport_name',
                  'service_level', 'hub_type',
                  'boardings', 'previous_year_boardings', 'yoy_change',)


# We enumerate all the headers in each file, even ones that won't be exported to output
HEADER_MAPS_PATH = Path('data', 'lookups', 'boardings_header_maps.json')


def cleanspace(txt):
    return re.sub(r'\s{2,}', ' ', txt).strip()

def get_year_header_map(year):
    # probably don't need to reopen this over and over, but whatever
    with open(HEADER_MAPS_PATH) as src:
        yr = str(year)
        maps = json.load(src)

    return next(m['headers'] for m in maps if yr in m['years'])


def process_file(srcpath):
    """
    Returns a list of dicts, including a key-value pair of year, based on the srcpath
    """
    fname = srcpath.stem
    year = re.match(r'^\d{4}', fname).group()
    headers = get_year_header_map(year)

    data = []
    with open(srcpath) as src:
        records = list(csv.reader(src))
        for row in records[1:]: # skip header row
            d = {h: cleanspace(row[i]) for i, h in enumerate(headers)}
            d['year'] = year
            if '_primary' in fname and not d.get('service_level'):
                d['service_level'] = 'P'
            data.append(d)

    return data



def main():
    DEST_PATH.parent.mkdir(exist_ok=True, parents=True)
    destfile = DEST_PATH.open('w')
    outs = csv.DictWriter(destfile, fieldnames=OUTPUT_HEADERS, restval=None, extrasaction='ignore')
    outs.writeheader()

    for srcpath in sorted(SRC_DIR.glob('*.csv')):
        stderr.write(f"Opening {srcpath}\n")
        data = process_file(srcpath)
        outs.writerows(data)
        stderr.write(f"\tWrote {len(data)} rows to {DEST_PATH}\n")

    destfile.close()

if __name__ == '__main__':
    main()

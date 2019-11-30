#!/usr/bin/env python

"""
collate_boardings.py

gather files from gather files from data/converted/boardings

Example usage:

$ scripts/collate/collate_boardings.py


- Remove ,$ from salary column
- collapse and strip whitespace
- unite them as data/collated/boardings.csv
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

            # for special cases, in which the filename denotes the type of airports
            #  and there is no service_level field
            if '_primary' in fname and not d.get('service_level'):
                d['service_level'] = 'P'

            # for some older XLS files, integer values in rank, boardings, and previous_year_boardings
            #   were converted to floats during the convert stage
            for _k in ('rank', 'boardings', 'previous_year_boardings'):
                val = d.get(_k)
                if val:
                    d[_k] = int(float(val))

            data.append(d)

    return data



def main():
    DEST_PATH.parent.mkdir(exist_ok=True, parents=True)
    destfile = DEST_PATH.open('w')
    outs = csv.DictWriter(destfile, fieldnames=OUTPUT_HEADERS, restval=None, extrasaction='ignore')
    outs.writeheader()

    rcount = 0
    for srcpath in sorted(SRC_DIR.glob('*.csv')):
        stderr.write(f"Opening {srcpath}\n")
        data = process_file(srcpath)
        stderr.write(f"\tProcessed {len(data)} rows\n")
        rcount += len(data)

        outs.writerows(data)

    destfile.close()
    stderr.write(f"{rcount} rows written to {DEST_PATH}\n")
if __name__ == '__main__':
    main()

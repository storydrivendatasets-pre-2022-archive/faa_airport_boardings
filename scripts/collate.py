#!/usr/bin/env python

"""
collate.py

gather files from data/stashed/processed.csv

- Remove ,$ from salary column
- collapse and strip whitespace
- unite them as data/collated/airport_annual_boardings.csv
"""
import csv
from pathlib import Path
import re

SRC_DIR = Path('data', 'stashed', 'processed')
DEST_PATH = Path('data', 'collated', 'airport_annual_boardings.csv')


Rank,RO,ST,Locid,City,Airport Name,S/L,Hub,CY 09 Boardings,CY 08 Boardings,% Change,,

OUTPUT_HEADERS = ('year', 'rank', 'region', 'state', 'airport_code', 'airport_name',
                  'airport_type', 'hub_type', 'enplanements', 'yoy_change')


def cleanspace(txt):
    return re.sub(r'\s{2,}', ' ', txt).strip()

# def process_file(srcpath):
#     """
#     yields a clean data row
#     """
#     year = srcpath.stem

#     try:
#         with open(srcpath, encoding='utf-8') as src:
#             # skip header, since layout is always the same
#             records = list(csv.reader(src))[1:]
#     except UnicodeDecodeError:
#         with open(srcpath, encoding='cp1252') as src:
#             records = list(csv.reader(src))[1:]


#     for row in records:
#         d = [year]
#         for idx, col in enumerate(row):
#             val = cleanspace(col)
#             if idx == SALARY_COL_IDX:
#                 val = re.sub(r'\$|,', '', val)
#             d.append(val)
#         yield d



# def main():
#     DEST_PATH.parent.mkdir(exist_ok=True, parents=True)
#     destfile = DEST_PATH.open('w')
#     outs = csv.writer(destfile)
#     outs.writerow(HEADERS)
#     for fn in sorted(SRC_DIR.glob('*.csv')):
#         for row in process_file(fn):
#             outs.writerow(row)
#     destfile.close()
#     print("Wrote", DEST_PATH.stat().st_size, 'bytes to', DEST_PATH)

# if __name__ == '__main__':
#     main()

#!/usr/bin/env python

import csv
from openpyxl import load_workbook
import re
from pathlib import Path
from sys import argv, stderr
from xlrd import open_workbook






def extract_csv(xlspath):
    if re.search(r'\.xls$', str(xlspath)):
        # old format; use xlrd
        # note that integers are wrongly typecasted to floats, but oh well
        sheet = open_workbook(xlspath).sheets()[0]
        ncols = sheet.row_len(0)
        nrows = sheet.nrows
        return [[sheet.cell_value(i, j) for j in range(ncols)] for i in range(nrows)]


    else:
        book = load_workbook(xlspath)
        return [[cell.value for cell in row] for row in book.active.rows]


if __name__ == '__main__':
    src_dir = Path(argv[1])
    dest_dir = Path(argv[2])
    dest_dir.mkdir(exist_ok=True, parents=True)

    files = sorted(src_dir.glob('*.xls*'))
    for fn in files:
        stderr.write(f"Reading {fn}\n")
        data = extract_csv(fn)
        destpath = dest_dir.joinpath(f'{fn.stem}.csv')
        stderr.write(f"\tWriting {len(data)} rows to: {destpath}\n")
        with open(destpath, 'w') as w:
            outs = csv.writer(w)
            outs.writerows(data)


# import code; code.interact(local=locals())

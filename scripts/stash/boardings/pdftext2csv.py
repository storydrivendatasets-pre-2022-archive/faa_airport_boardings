#!/usr/bin/env python

"""
Year 2000 They were converted to text via pdftotext -layout

This script uses the magic of regex to delimit the data so we can get a CSV out of it.

This script also adds headers to the parsed CSV
"""

import csv
from pathlib import Path
import re
from sys import argv, stderr


"""
#   Example raw text data lines:

  1    ATL    THE WILLIAM B HARTSFIELD AT   ATLANTA                GA     39,277,901
  2    ORD    CHICAGO O'HARE INTL           CHICAGO                IL     33,845,895
418    MTM    METLAKATLA                    METLAKATLA             AK         10,027
419    MTH    THE FLORIDA KEYS MARATHON     MARATHON               FL         10,011

The pattern:
    - rank: start of line, one-or-more whitespaces, then 1-or-more digits
    - airport_code: 1-or-more-whitespaces, then exactly 3 uppercase letters or numbers
    - airport_name: 3-or-more-whitespaces, then any mix of characters until hitting 3-or-more whitespaces
    - city: 3-or-more-whitespaces, then any mix of characters until hitting 3-or-more whitespaces
    - state: exactly 2 uppercase letters
    - enplanements: 1-or-more digits-or-commas, followed by 0-or-more whitespaces, then end-of-line
"""

RX_DATA_LINE = (
                r'^\s*(?P<rank>\d+)\s+'
                + r'(?P<airport_code>[A-Z0-9]{3})\s+'
                + r'(?P<airport_name>.+?)\s{3,}'
                + r'(?P<city>.+?)\s{3,}'
                + r'(?P<state>[A-Z]{2})\s{3,}'
                + r'(?P<enplanements>[\d,]+)\s*$'
               )

"""
 Rnk LOCID Airport (City, State)                    CY2000     Change      CY1999
   1 ATL THE WILLIAM B HARTSFIE(ATLANTA,GA)       39,277,901      3.0%   38,136,866
   2 ORD CHICAGO O'HARE INTL(CHICAGO,IL)          33,845,895     -0.6%   34,050,083

"""

RX_YOY_DATA_LINE = (
                r'^\s*(?P<rank_2000>\d+)\s+'
                + r'(?P<airport_code>[A-Z0-9]{3})\s+'
                + r'(?P<airport_name>[^(]+)\('
                + r'(?P<city>.+?),(?=[A-Z]{2}\))'
                + r'(?P<state>[A-Z]{2})\)\s+'
                + r'(?P<enplanements_2000>[\d,]+)\s+'
                + r'(?P<yoy_change>[\-0-9\.]+%)\s+'
                + r'(?P<enplanements_1999>[\d,]+)\s*$'
               )


def process_line(line, data_pattern):
    """
    line is a plaintext string, straight from the pdftotext -layout formatted text file
    data_pattern is a string that represents a regex pattern for a data line
    Returns:
        - None if the line is perceived to be a non-data line, such as a header
        - a dict of strings

    """
    mx = re.match(data_pattern, line)
    if mx:
        return mx.groupdict()
    else:
        # if line.strip():
        #     print(line)
        return None


def process_textfile(srcpath, data_pattern):
    """
    srcpath is a path to a text file, presumably from pdftotext

    data_pattern is a string that represents a regex pattern for a data line

    Returns: a list of dicts
    """

    data = []
    for line in srcpath.open():
        record = process_line(line, data_pattern)
        if record:
            data.append(record)
    return data



def main():
    srcdir = Path(argv[1])
    destdir = Path(argv[2])
    destdir.mkdir(exist_ok=True, parents=True)
    for srcpath in srcdir.glob('*.pdf.txt'):

        stderr.write(f"Opening {srcpath}\n")
        if 'yoy_change' in str(srcpath):
            data = process_textfile(srcpath, data_pattern=RX_YOY_DATA_LINE)
        else:
            data = process_textfile(srcpath, data_pattern=RX_DATA_LINE)

        destpath = destdir.joinpath(f'{srcpath.stem}.csv')
        stderr.write(f"Writing {len(data)} rows to {destpath}\n")
        with open(destpath, 'w') as w:
            outs = csv.DictWriter(w, fieldnames=data[0].keys())
            outs.writeheader()
            outs.writerows(data)


if __name__ == '__main__':
    main()

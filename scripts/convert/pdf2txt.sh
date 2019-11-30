#!/bin/sh
# example call:
#
#  ./scripts/stash/pdf2txt.sh  data/stashed/boardings  data/converted/boardings

SRC_DIR=$1
DEST_DIR=$2

mkdir -p $DEST_DIR

find ${SRC_DIR} -name *.pdf | while read -r pdfname; do
    txtname=${DEST_DIR}/$(basename $pdfname).txt
    >&2 echo Extracted: ${txtname}
    >&2 echo "     from:" ${pdfname}

    pdftotext -layout ${pdfname} - > ${txtname}
done

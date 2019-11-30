.DEFAULT_GOAL := help
.PHONY : clean help ALL

SQLIZED_DB = data/sqlized.sqlite
STASHED_FILES = data/stashed/boardings/2018.xlsx \
				data/stashed/boardings/1999_primary_yoy_change.pdf

CONVERTED_BOARDINGS = data/converted/boardings/2018.csv \
			      data/stashed/boardings/1999_primary_yoy_change.pdf.csv

CONVERTED_FILES = $(CONVERTED_BOARDINGS) \
				  data/converted/airports.csv \
				  data/converted/runways.csv
help:
	@echo 'Run `make ALL` to see how things run from scratch'

ALL: clean sqlize


clean_start: clean
	rm -rf data/stashed

clean:
	@echo --- Cleaning
	rm -rf data/converted
	rm -rf data/collated
	rm -rf data/wrangled
	rm -f $(SQLIZED_DB)

# change sqlize task to do something else besides sqlize_bootstrap.sh,
# when you need something more sophisticated
sqlize: $(SQLIZED_DB)

# create data/sqlized/mydata.sqlite from CSVs in wrangled
$(SQLIZED_DB): wrangle
	@echo ""
	@echo --- Building $@
	@echo
	./scripts/sqlizeboot.sh \
		$(SQLIZED_DB) \
		data/wrangled


## collate stuff
collate: collate_boardings

collate_boardings: data/collated/boardings.csv

data/collated/boardings.csv: scripts/collate/collate_boardings.py data/converted/boardings

	./scripts/collate/collate_boardings.py



## stash stuff


convert: $(CONVERTED_FILES)


$(CONVERTED_FILES): stash
	@echo "converting airports and runways"
	./scripts/convert/excel2csv.py \
		data/stashed \
		data/converted


	@echo "converting boardings"
	./scripts/convert/excel2csv.py \
		data/stashed/boardings \
		data/converted/boardings

	echo ""
	./scripts/convert/pdf2txt.sh \
		data/stashed/boardings \
		data/converted/boardings

	echo ""
	./scripts/convert/pdftext2csv.py \
		data/converted/boardings \
		data/converted/boardings

stash: $(STASHED_FILES)
# only run this when you need to do a full refresh of the source data
# for some reason


$(STASHED_FILES): ./scripts/stash_files.py

	./scripts/stash_files.py




.DEFAULT_GOAL := help
.PHONY : clean help ALL manual_fix

SQLIZED_DB = data/faa_airport_boardings.sqlite





STASHED_FILES =  data/stashed/boardings/2018.xlsx \
				data/stashed/boardings/1999_primary_yoy_change.pdf \
				data/stashed/airport_data/airports.xls \
			    data/stashed/airport_data/runways.xls







help:
	@echo 'Run `make ALL` to see how things run from scratch'

ALL: clean sqlize

REBOOT: clean_start ALL

# only do this when you want to fetch (and manually fix) data from the source
clean_start: clean
	rm -rf data/stashed/boardings
	rm -rf data/stashed/airport_data


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
	./scripts/sqlize/sqlizeboot.sh \
		$(SQLIZED_DB) \
		data/wrangled

wrangle: collate
	@echo "just a stub"
	mkdir -p data/wrangled
	cp data/collated/*.csv data/wrangled


## collate stuff
collate: collate_airport_data collate_boardings

collate_airport_data: data/converted/airport_data
	./scripts/collate/collate_airport_data.py


collate_boardings: data/collated/boardings.csv
data/collated/boardings.csv: scripts/collate/collate_boardings.py data/converted/boardings

	./scripts/collate/collate_boardings.py






## stash stuff


convert: convert_airport_data convert_boardings


convert_airport_data: data/converted/airport_data/
data/converted/airport_data: stash
	@echo "converting airport data"
	./scripts/convert/excel2csv.py \
		data/stashed/airport_data/manual_fix \
		data/converted/airport_data

convert_boardings: data/converted/boardings/
data/converted/boardings: stash
	@echo "converting boardings"
	./scripts/convert/excel2csv.py \
		data/stashed/boardings \
		data/converted/boardings

	@echo "...pdfs to text"
	./scripts/convert/pdf2txt.sh \
		data/stashed/boardings \
		data/converted/boardings

	@echo " ...texts to csv"
	./scripts/convert/pdftext2csv.py \
		data/converted/boardings \
		data/converted/boardings




stash: $(STASHED_FILES) manual_fix
# only run this when you need to do a full refresh of the source data
# for some reason

# The airports.xls and runways.xls spreadsheets can't be opened with our automated scripts, owing to
#   a broken Excel export from the FAA. So whenever we download these files, we need to manually
#   convert them to xlsx, and save them to data/stashed/airport_data/manual_fix
manual_fix: data/stashed/airport_data/manual_fix/airports.xlsx \
			data/stashed/airport_data/manual_fix/runways.xlsx

data/stashed/airport_data/manual_fix/airports.xlsx: data/stashed/airport_data/airports.xls
	@echo "NOTE: You must manually open, with Excel, the file:   $?"
	@echo "                And save it into a newer format as:   $@"
	exit 1

data/stashed/airport_data/manual_fix/runways.xlsx: data/stashed/airport_data/runways.xls
	@echo "NOTE: You must manually open, with Excel, the file:   $?"
	@echo "                And save it into a newer format as:   $@"
	exit 1

$(STASHED_FILES): ./scripts/stash_files.py
	./scripts/stash_files.py




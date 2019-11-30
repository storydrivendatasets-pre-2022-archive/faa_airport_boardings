.DEFAULT_GOAL := help
.PHONY : clean help ALL \
	stash process_stash fetch_stash

SQLIZED_DB = data/sqlized.sqlite


help:
	@echo 'Run `make ALL` to see how things run from scratch'

ALL: clean sqlize


clean:
	@echo --- Cleaning
	rm -f
	rm -rf data/stashed/processed
	rm -f data/wrangled/hello.csv


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


## stash stuff
stash: fetch_stash process_stash

process_stash:
	@echo "processing boardings data"
	./scripts/stash/boardings/excel2csv.py \
		data/stashed/originals/boardings \
		data/stashed/processed/boardings

	./scripts/stash/boardings/pdf2txt.sh \
		data/stashed/originals/boardings \
		data/stashed/processed/boardings

	echo ""
	./scripts/stash/boardings/pdftext2csv.py \
		data/stashed/processed/boardings \
		data/stashed/processed/boardings


# only run this when you need to do a full refresh of the source data
# for some reason
fetch_stash:
	./scripts/stash/fetch_files.py


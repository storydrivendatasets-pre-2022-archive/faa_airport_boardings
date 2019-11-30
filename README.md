# FAA Annual Passenger Boardings for Primary Airports

This repo collects and wrangles FAA boarding data from 2000 to 2018 for each primary (i.e. main) airport.

https://www.faa.gov/airports/planning_capacity/passenger_allcargo_stats/passenger/


It also has metadata for each airport and runway:

https://www.faa.gov/airports/airport_safety/airportdata_5010/menu/nfdcrunwaysexport.cfm?Region=&District=&State=&County=&City=&Use=PU&Certification=

Source file manifest: [data/data_manifest.yaml](data/data_manifest.yaml)


## Being a developer

To run the Python scripts, you'll need to load the dependencies in [requirements.txt](requirements.txt)

```sh
pip install -r requirements.txt
```

To build the wrangled and sqlized data (i.e. `data/faa_airport_boardings.sqlite`) from the data stored in [data/stashed](data/stashed), run:

```sh
make ALL
```

To fetch the data from the FAA website – which necessitates manually fixing the [data/stashed/airport_data/manual_fix/airports.xls](data/stashed/airport_data/manual_fix/airports.xls) and [data/stashed/airport_data/manual_fix/runways.xls](data/stashed/airport_data/manual_fix/runways.xls), run:

```sh
make REBOOT
```

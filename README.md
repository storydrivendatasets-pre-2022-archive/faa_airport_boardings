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

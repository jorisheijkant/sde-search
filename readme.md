# SDE search
Search the enormous Dutch SDE subsidies xml file in a more convenient way. You can search for a company, after which the code will output a csv file regarding all the subsidies for this company.

## Prerequisites and usage
You need Python installed for this script. There's no dependencies you need to install. Just run `python3 search-company [COMPANY NAME]`. The script will output a csv file with all the subsidies for this company in the `data/output` folder.

## Data not included
The actual SDE xml is 80mb and not included in this repository. You can download it [here](https://data.rvo.nl/sites/default/files/open_data/dop_projecten.xml) and put it in the data file as `sde.xml`.

The data will be updated from time to time. As long as the underlying data structure does not change, the code should work.
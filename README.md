# CA-fires
* A python script to extract historical fire damage data from a CAL FIRE incident report in pdf format into a .csv flat file.

* Output flat file containes yearly data on number of fires, acres burned and damage in dollars,
from 1933 to 2016, the latest data available in the report.

* This script depends on the [tabula-py](https://github.com/chezou/tabula-py) package, a simple wrapper of tabula-java: extract table from PDF into pandas DataFrame.

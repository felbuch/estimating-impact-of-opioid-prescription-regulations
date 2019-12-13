### Raw data on Drug Shipment is on a level of individual shipments.
### The analysis we wish to perform is on the level of a county.
### Hence, we must group shipment observations by buyer's county in a given year.
### This script imports the Drug Shipment data and performs this group by.
### It returns a pandas dataframe with the county, the year and the total number of units
### shipped to that county in that year.
### For our analysis, it shall be further necessary to filter the necessary years.
### However, since each analysis requires a different set of years, we do not filter by years
### in this script.

#Import packages
import os
import pandas as pd

#Change working directory

os.chdir("C:/Users/Joe Krinke/Desktop/")

#Import data on shipments - Using a subset of the data
shipments = pd.read_csv("shipments.csv")

#Define function to extract year from transaction date
def get_year(date):
    date = str(date)
    year = date[-4:]
    return(year)

#Create variable with year of transaction
shipments['YEAR'] = list(map(get_year, shipments['TRANSACTION_DATE']))

#Select columns we are interested in keeping
shipments = shipments.loc[:,['BUYER_COUNTY','BUYER_STATE', 'YEAR','QUANTITY','MME_Calculated']]

#Group by buyer-county per year
shipments = shipments.groupby(['BUYER_COUNTY','BUYER_STATE','YEAR'],axis = 0, as_index = False).sum()

#Save shipments by county & year as parquet file
shipments.to_parquet("shipments_by_county.gzip")


###Add FIPS to (grouped) shipment data
###This script gets data on shipment data by county and year 
###and adds the FIPS code to each county.
###To this end, it uses the addfips package.
###For reference on the addfips package see:
###################################
#https://pypi.org/project/addfips/
###################################

import os
import pandas as pd
import addfips #This package adds FIPS info to a dataframe containing a column of county names

#Change working directory
os.chdir("C:/Users/Felipe/Desktop/Duke MIDS/Practical Tools in Data Science/")

#Open file
shipments = pd.read_parquet("shipments_by_county.gzip")


#We now define two functions we'll need to use:

def series_to_dict(series):
    
    '''The addfips package requires the info on the county to be passed as a dictionary.
    This is an auxiliary function that will take a row of the shipment dataframe (a series)
    and transform it into a dictionary.'''
    
    output = {} #Start with an empty dictionary
    for i in range(len(series)): #For every element in the series...
        key = series.index[i] #... get the dataframe's column name and save it as a key
        value = series[i] #... get the value of that column ans save it as the value associated to that key...
        output.update({key:value}) #... and put the key-value pair as an element in the dictionary
    return(output)

def get_fips(row):
    
    '''This function gets a row from a dataframe (a series) and returns the FIPS code from the county.'''
    
    af = addfips.AddFIPS()
    row_as_dict = series_to_dict(row)
    row_with_fips = af.add_county_fips(row_as_dict,county_field="BUYER_COUNTY",state_field="BUYER_STATE")
    fips = row_with_fips['fips']
    return(fips)

#We create a list with the fips of the counties in our dataframe
#This list will be attached to the dataframe as a new FIPS column
list_of_fips = []
for index, row in shipments.iterrows():
    fips = get_fips(row)
    list_of_fips.append(fips)

assert len(list_of_fips) == len(shipments)

#Attach FIPS as a new column to the shipments dataset
shipments['FIPS'] = list_of_fips

#Some tests cases
#shipments[shipments.FIPS == '04013'] #Maricopa, AZ
#shipments[shipments.FIPS == '36089'] #Saint Lawrence, NY

#Save dataset
shipments.to_parquet('shipments_with_FIPS.gzip')

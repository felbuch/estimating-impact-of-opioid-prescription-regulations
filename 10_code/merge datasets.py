### In this script, we merge three datasets:
### (1) Shipments of drugs for each county
### (2) Population of each county
### (3) Causes of death in each county
### This script is divided in three parts.
### In part 1, we merge the shipments and population datasets (1 and 2)
### In part 2, we merge the dataset obtained in part 1 with the causes od death (3) dataset.
### In part 3, we aggregate at the level of state-year and calculate the number of deaths per 100k inhabitants


import os
import pandas as pd
import numpy as np

#This function will help us avoid mistakes
def is_primary_key(data_frame, key):
    '''This function returns TRUE if the columns listed in key
    constitute a primary key to the given dataframe and false otherwise.
    Hence, if we expect a dataframe to have one row per county-year,
    then passing the dataframe with key = ['county','year'] should return
    TRUE if everything is ok'''

    number_of_rows = len(data_frame)

    df = data_frame.loc[:,key]
    df = df.drop_duplicates()
    number_of_unique_rows = len(df)

    return (number_of_rows == number_of_unique_rows)


#Now lets start the merging process:

#Open populations file
os.chdir("C:/Users/Felipe/Desktop/Duke MIDS/Practical Tools in Data Science/estimating-impact-of-opioid-prescription-regulations-team-8/20_intermediate_files")
population = pd.read_csv("population data with FIP in long format.csv", encoding='latin-1')

#Select relevant columns
population = population.loc[:,['FIP','Year','population']]

assert is_primary_key(population, ['FIP','Year'])
assert 2010 in(population.Year)

#Filter population for year 2010
#We would not like to do this and, in the future, may consider alternatives to this approach.
#However, our population dataset has years 2010-2018 and our shipment dataset has years 2006-2012.
#So the overlap between the two is so small, that we believe we do best in simply considering the
#population fixed as in 2010.
#We may later improve our model by searching a dataset with county population in 2006-2012
population = population.loc[population.Year == 2010]
assert population.Year.drop_duplicates().values == 2010

#Since we are only considering population in 2010, there is no point in keeping
#track of the year as a variable.
#Likewise, the year ceases to be part of the primary key.
#This will entail significant differences in our code
#relative to the version we had before.
#Therefore, if -- or when -- we decide to search for a new dataset on population,
#we should consider reversing to a previous comit of this code.
#This being said, let's drop Year from the population dataset
#and consider only FIPS as its primary key.
population = population.drop('Year', axis = 1)
assert is_primary_key(population, 'FIP')

#Open shipments file
os.chdir("C:/Users/Felipe/Desktop/Duke MIDS/Practical Tools in Data Science/")
shipments = pd.read_parquet("shipments_with_FIPS.gzip")
assert shipments.YEAR.min() <= 2006
assert shipments.YEAR.max() >= 2012
assert 2010 in shipments.YEAR

#Our problem specification tells us to drop Alaska, so we will.
#Sorry, Alaska. I know I'm cold-blooded.
is_Alaska = shipments[shipments.BUYER_STATE == "AK"].index
shipments.drop(is_Alaska, axis = 0, inplace=True)

#Some counties have missing FIPS:
#shipments.loc[shipments.FIPS.isnull(),['BUYER_STATE','BUYER_COUNTY','FIPS']]
#We should not drop them. But we will, for now.
shipments = shipments.dropna(subset = ['FIPS'])

#We'll proffit from the opportunity to drop some columns we no longer need
shipments = shipments.drop(['CALC_BASE_WT_IN_GM','MME_Conversion_Factor'], axis = 1)

#We would like to have one row per FIPS per year. We do not:
#assert is_primary_key(shipments, ['FIPS','YEAR']) #Throws an error!
#Our shipment data has multiple lines associated with the same FIPS.
#An example is Baltimore and Baltimore City. Let's fix this.
shipments = shipments.drop('BUYER_COUNTY', axis = 1)
shipments = shipments.groupby(['FIPS','YEAR','BUYER_STATE'], as_index=False).sum()
#(we keep buyer state because we will later on want to group by this)

assert is_primary_key(shipments, ['FIPS','YEAR'])

#Rename population column to match shipment
population.rename(columns = {'FIP':'FIPS'}, inplace = True)

#Adjust shipment FIPS and YEAR to numpy int64 for matching
shipments.FIPS = np.int64(shipments.FIPS)
shipments.YEAR = np.int64(shipments.YEAR)

assert type(shipments.FIPS[0]) == type(population.FIPS[0])

#Merge
data = pd.merge(shipments, population, on = ['FIPS'], how = 'inner', indicator=True, validate='m:1')

#Check if merge was succesful
assert len(data.loc[data._merge != 'both']) == 0, "Some counties were only present in one dataset, not on both"
data = data.drop('_merge', axis = 1) #Column _merge is no longer useful and will be a nuissance on our next merge, so let's drop it
assert is_primary_key(data,['FIPS','YEAR'])
assert (data.YEAR.min() <= 2006) and (data.YEAR.max() >= 2012)

##########
# Part 2 #
##########

cod = pd.read_parquet("Causes_of_Death_ready_to_merge.gzip")

#Make necessary adjustments in table to allow merging
cod = cod.rename(columns = {'Year':'YEAR'}) #Change 'year' column in *cod* dataframe to match *data* dataframe
data = data.astype({'YEAR':'int64'}) #Change *year* from string to int64
cod = cod.astype({'YEAR':'int64'}) #Change *year* from float64 to int64

assert np.dtype(cod.YEAR) == np.dtype(data.YEAR)
assert is_primary_key(cod, ['FIPS','YEAR'])

#Merge
data = pd.merge(data, cod, on = ['FIPS','YEAR'], how = 'inner', indicator=True)
assert len(data.loc[data._merge != 'both']) == 0, "Some counties were only present in one dataset, not on both"
data = data.drop('_merge', axis = 1) #Column _merge is no longer useful so let's drop it
assert is_primary_key(data,['FIPS','YEAR'])


#Rename columns in final dataset
data = data.rename(columns={'BUYER_STATE':'STATE'})

##########
# Part 3 #
##########

#Convert numbers coded as strings into floats to allow for summation
data = data.astype({'Deaths':'float','population':'float'})

#Drop unnecessary columns for groupby
data = data.drop(columns = ['FIPS'], axis = 1)

#Groupby
data = data.groupby(['STATE','YEAR'], as_index = False).sum()
assert is_primary_key(data,['STATE','YEAR'])

#Create death per capita variable
data['deaths_per_100k'] = 100000* data['Deaths'] / data['population']

#Save
os.chdir("./estimating-impact-of-opioid-prescription-regulations-team-8/20_intermediate_files")
data.to_parquet("merged_data_pop2010.gzip")

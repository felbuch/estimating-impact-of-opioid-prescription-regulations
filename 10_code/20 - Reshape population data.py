#Reshape population dataset
#We have population estimates per county in wide format (one column per year)
#We wish to reshape this into long format (one row per county-year)

import os
import pandas as pd
import numpy as np

#Open populations file
os.chdir("C:/Users/Felipe/Desktop/Duke MIDS/Practical Tools in Data Science/estimating-impact-of-opioid-prescription-regulations-team-8/20_intermediate_files")
population = pd.read_csv("population data with FIP.csv", encoding='latin-1')

#Select relevant columns
population = population.loc[:,['FIP',
                               'POPESTIMATE2010',
                              'POPESTIMATE2011',
                              'POPESTIMATE2012',
                              'POPESTIMATE2013',
                              'POPESTIMATE2014',
                              'POPESTIMATE2015',
                              'POPESTIMATE2016',
                              'POPESTIMATE2017',
                              'POPESTIMATE2018']]

#Reshape. Our unit id's are the countys (FIPS) and the values associated to them
#are their populations at each year
population = population.melt(id_vars = ['FIP'] ,value_vars = ['POPESTIMATE2010',
'POPESTIMATE2011',
'POPESTIMATE2012',
'POPESTIMATE2013',
'POPESTIMATE2014',
'POPESTIMATE2015',
'POPESTIMATE2016',
'POPESTIMATE2017',
'POPESTIMATE2018'])

#Define function to get the year from string like 'POPESTIMATE2010'.
#It should return 2010.
def get_year(string_with_year_at_the_end):
    return(string_with_year_at_the_end[-4:])

#Apply function
population['variable'] = population['variable'].apply(get_year)

#Give more meaningful names to the columns
population = population.rename(columns = {'variable':'Year', 'value':'population'})

#Save
population.to_csv("population data with FIP in long format.csv")

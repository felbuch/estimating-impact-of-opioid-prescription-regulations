# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 14:02:52 2019

@author: Felipe
"""

import pandas as pd
import os

project_directory = "C:/Users/Felipe/Desktop/Duke MIDS/Practical Tools in Data Science/estimating-impact-of-opioid-prescription-regulations-team-8"
course_directory = "C:/Users/Felipe/Desktop/Duke MIDS/Practical Tools in Data Science/"
#os.chdir(project_directory)
os.chdir(course_directory)


### I'll temporarily copy the code of a function
### I'd like to be importing here. 
### (while I don't figure out how to actually import it)

def combine_state_and_county_into_FIP_code(state, county):
    
    '''Gets code from a state and a county and concatenates
    them in order to produce the corresponding FIP number of a county.
    If a county has only one or two digits, this function fills
    the missing zeros so that the FIP number achieves 4 or 5 digits.
    If it is the state that has a single digit, however, this function
    does NOT supply a leading zero. Therefore, the final FIP number
    returned as an output can have either 4 or 5 digits.'''
    
    #Transform everything to string, so we can count the number of digits
    #and concatenate leading zeros
    state = str(state)
    county = str(county)
    
    assert len(state) > 0, "The state code is missing or couldn't be converted into a string."
    assert len(county) > 0, "The county code is missing or couldn't be converted into a string"
    assert len(state) <= 2, "State has code with more than two digits. State codes must have at most 2 digits."
    assert len(county) <= 3, "County has code with more than three digits. County codes must have at most 3 digits."
    
    #Add leading zeros to the county code until it has three digits.
    while len(county) < 3:
        county = "0" + county
    #Note that we do not add leading zeros to the state level.    
    
    #Produce the FIP code by concatenating state and county
    FIP = state + county
    return(FIP)

#########################################################

#Load populations dataset
pop = pd.read_csv("County Population Data.csv", encoding = "latin-1")
pop['FIP'] = 0

for i in range(len(pop)):
    
    state = pop['STATE'][i]    
    county = pop['COUNTY'][i]
    pop.loc[:,'FIP'][i] = combine_state_and_county_into_FIP_code(state, county )
    

output_file_name = "population data with FIP"
pop.to_csv(project_directory + "/20_intermediate_files/" + output_file_name  + ".csv")

    



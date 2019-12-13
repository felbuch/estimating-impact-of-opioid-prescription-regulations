# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 13:08:09 2019

@author: Felipe
"""

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
    
def test_combine_state_and_county_into_FIP_code(state, county, expected_result):
    actual_result = combine_state_and_county_into_FIP_code(state, county)
    if actual_result == expected_result:
        pass
    else:
        print("ERROR! For state = {} and county = {}, expected {} but got {}".format(state, county, expected_result, actual_result))
        pass




test_combine_state_and_county_into_FIP_code(1,126,"1126")
test_combine_state_and_county_into_FIP_code(1,123,"1123")
test_combine_state_and_county_into_FIP_code(31,415,"31415")
test_combine_state_and_county_into_FIP_code("1","123","1123")

#Expected error cases:
#test_combine_state_and_county_into_FIP_code(11,1264,"11264")
#test_combine_state_and_county_into_FIP_code(1,1264,"11264")


    
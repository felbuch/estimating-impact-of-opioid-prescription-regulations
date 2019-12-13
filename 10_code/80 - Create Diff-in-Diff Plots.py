import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from plotnine import *
import gzip

data = pd.read_parquet("merged_data_pop2010.gzip")

'''
This code produces difference-in-difference plots for policy interventions in Florida, Texas, and Washington. 
Each state is compared to the rest of the United States in each plot

### Reading in data 

df = pd.read_parquet('merged_data.gzip')
df.head()

##Processing data. No longer needed with waht we are using now. 
#df['Deaths'] = df['Deaths'].astype('float')
#df['POPESTIMATE2010'] = df['POPESTIMATE2010'].astype('float')
#df.drop(['COUNTY', 'FIPS'], axis = 1)


### Calculating per capita Drugs

df['DrugsPerCapita'] = df['MME_Calculated']/df['population']
    
    
###Start by subsetting data by years. The analysis will be completed using all available data for that specific area. 
###The following function subsets data by years. 

def year_subset(df, start, end) : 

    boolean_years = (df['YEAR'] > start) & (df['YEAR'] <= end)
    filtered_data = df[boolean_years]
    return(filtered_data)
    
    
###This function produces difference in differnce plots. You can specify the year of the policy and the variable you're interested in. 

def diff_in_diff(data, state, year_change, response):

    data_before = year_subset(data, 2006, year_change)
    data_before['InState'] = data_before['STATE']==state
    data_before = data_before.groupby(['YEAR', 'InState'], as_index=False).mean()
    data_after = year_subset(data, year_change, 2020)
    data_after['InState'] = data['STATE']==state
    data_after = data_after.groupby(['YEAR', 'InState'], as_index=False).mean()

    before =(ggplot(data_before, aes(x='YEAR', y= response, group = 'InState')) + geom_line(alpha=.5) + geom_point()+ggtitle('Before Intervention'))
    after = (ggplot(data_after, aes(x='YEAR', y= response, group = 'InState')) + geom_line(alpha=.5) + geom_point()+ggtitle('After Intervention'))
    print(before)
    print(after)

def pre_post_graph(state, year_of_treatment, df = data, path = 'C:\\Users\\Felipe\\Desktop\\Duke MIDS\\Practical Tools in Data Science\\estimating-impact-of-opioid-prescription-regulations-team-8\\30_results'
):

'''This functions makes the pre_post analysis graph for a state which has gone through
a policy change in the year of treatment.
This function both plots the graph and saves it as a jpg file in the folder listed in path.'''

    treated = df.loc[df.STATE == state,['YEAR','deaths_per_100k']]
    control = df.loc[df.STATE != state,['YEAR','deaths_per_100k']].groupby('YEAR', as_index = False).mean()

    fig = plt.figure()
    plt.plot(treated.YEAR, treated.deaths_per_100k, marker = 'o', color = 'red')
    plt.plot(control.YEAR, control.deaths_per_100k, marker = 'o', color = 'blue')
    plt.ylim(0,15)
    plt.axvline(x = year_of_treatment, linestyle = "dashed")
    plt.legend([state,'other states'])
    plt.xlabel('Year')
    plt.ylabel('Deaths per 100k people')
    plt.title(state)
    #plt.show()

    os.chdir(path)
    fig.savefig(state + ".jpg")
    pass

os.getcwd()
#Now lets run our function for the cases we wish to analyse
pre_post_graph('FL',2010)
pre_post_graph('WA',2012)
pre_post_graph('TX',2007)



data.describe()

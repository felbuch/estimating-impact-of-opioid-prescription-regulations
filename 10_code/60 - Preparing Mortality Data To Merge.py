import os
import pandas as pd
import numpy as np

#Open file
os.chdir("C:/Users/Felipe/Desktop/Duke MIDS/Practical Tools in Data Science/")
cod = pd.read_csv("drug_data_full.csv") #Cause of death

#cod.sample(3)
#cod['Drug/Alcohol Induced Cause'].value_counts()

#Create list with death causes we wish to analyse
#I only comment the ones we do not want, so we can easily
#add new ones, if we wish to. All we'll have to do is
#un-comment the ones we wish to add.
prescription_overdose = [
'Drug poisonings (overdose) Unintentional (X40-X44)',
#'All other alcohol-induced causes',
#'Drug poisonings (overdose) Suicide (X60-X64)',
#'Drug poisonings (overdose) Undetermined (Y10-Y14)',
#'All other drug-induced causes' #,
#'Alcohol poisonings (overdose) (X45, X65, Y15)',
#'Drug poisonings (overdose) Homicide (X85)'
]

#Filter rows refering to the causes of death we are interested in
cod = cod[cod['Drug/Alcohol Induced Cause'].isin(prescription_overdose)]


#Remove unnecessary columns
cod = cod.loc[:,['County Code','Year','Deaths']].copy()

#Transform County Code to numpy int64 type
cod['County Code'] = np.int64(cod['County Code'])

#Group by county and year, adding the total number of deaths.
#This step is unnecessary if we're dealing with only one cause of death,
#but we code it nonetheless, to prevent errors in merging should we wish to consider
#more than a single cause of death.
cod = cod.groupby(['County Code','Year'],as_index = False).sum()

#Rename County Code to FIPS
cod = cod.rename(columns = {'County Code':'FIPS'})

#Save dataset
cod.to_parquet("Causes_of_Death_ready_to_merge.gzip")

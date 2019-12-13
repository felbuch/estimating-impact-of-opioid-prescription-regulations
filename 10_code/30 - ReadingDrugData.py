''' Reading in and looking at a subset of the data to see which columns we want '''
import pandas as pd
subset = pd.read_csv('Copy of SubsetRows.csv',encoding='latin-1')
#subset.head()

''' Creating a list of the columns we want to keep in this dataset '''

subset_columns = ['BUYER_STATE', 'BUYER_COUNTY', 'TRANSACTION_DATE','CALC_BASE_WT_IN_GM','MME_Conversion_Factor']

'''Reading in the data through chunking and dropping variables.  '''

os.chdir("C:/Users/Joe Krinke/Desktop/Nick's Opoid Project")

tempChunk =[]
tempData = []
shipments = pd.DataFrame()
chunksize = 10 ** 7
drug_data = pd.DataFrame()
for chunk in pd.read_csv('arcos_all_washpost.tsv', sep='\t', chunksize = chunksize, iterator =True , low_memory=False):
    shipments = chunk.loc[:,subset_columns]
    tempData.append(shipments)
''' Buffering Chunks'''
shipments = pd.concat(tempData)

'''Getting Years'''
shipments['YEAR'] = shipments['TRANSACTION_DATE'][-4:]

''' Calculating standardized drug quantities'''
### Converting type to float
shipments['MME_Conversion_Factor'] = shipments['MME_Conversion_Factor'].astype(float)
shipments['CALC_BASE_WT_IN_GM'] = shipments['CALC_BASE_WT_IN_GM'].astype(float)


##Calculating MME
shipments['MME_Calculated'] = shipments.loc[:,'MME_Conversion_Factor']*shipments.loc[:,'CALC_BASE_WT_IN_GM']

## dropping variables not required on our further research
shipments = shipments.drop(['QUANTITY', 'CALC_BASE_WT_IN_GM', 'DOSAGE_UNIT', 'MME_Conversion_Factor','dos_str'], axis = 1)

## Dropping Alaska state due to the weird thingy going on
shipments = shipments[(shipments['STATE'] != 'AK')]

##Exporting file.
shipments.to_parquet('shipments.gzip')''' Creating a list of the columns we want to keep in this dataset '''

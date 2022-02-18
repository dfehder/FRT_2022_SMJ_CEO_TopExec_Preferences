"""
CREATE DATE: 7/9/2021
CREATED BY: DANIEL FEHDER
DESCRIPTION: Automated creation of subset files
"""
import pandas as pd
import numpy as np
import os
import sys
from collections import defaultdict
from dotenv import load_dotenv

# for now explicitely set the dotenv path. There are ways to make this slicker to not
# require an explicit reference but you need to think about execution environment and architecture
#local env path
#dotenv_path = "/Users/danielfehder/dev/frt_2021b/.env"
#cluster env path
dotenv_path = "/project/fehder_718/frt_2021b/.env"

# load environmental variables
load_dotenv(dotenv_path)

# file locations (make sure paths exist before run)
# path of where to get data
floc = os.getenv("L2_INTER_DIR")
# path for where the data goes
dloc = floc + 'combined/'
#dsets = ['preferences_raw', 'demographics_raw']

raw_states = os.listdir(floc)
statemap = {'1':['AK', 'AL', 'AR', 'AZ', 'CA', 'CO'], 
            '2':['CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL'], 
            '3':['IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO'], 
            '4':['MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY'], 
            '5':['OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN'], 
            '6':['TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']}


# get the data set reference we are working with
dset = sys.argv[1]
sind = sys.argv[2]
print(dset)
print(sind)

# get the filtered set of files to process
allsets = [elem for elem in raw_states if dset in elem]
allsets = [elem for elem in allsets if elem[:2] in statemap[sind]]


print(allsets)

# initialize the datasets through list comprehension
dflist = [pd.read_pickle("%s%s"%(floc, elem)) for elem in allsets]


# combine the datasets
df = pd.concat(dflist)

print(len(df))

# now export
df.to_csv('%scombine_inter_%s_%s.csv'%(dloc, dset, sind), index=False)


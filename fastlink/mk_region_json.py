"""
CREATE DATE: 10/29/2021
CREATED BY: DANIEL FEHDER
DESCRIPTION: Automated creation of subset files
"""
import pandas as pd
import os
from dotenv import load_dotenv
import json

#cluster env path
dotenv_path = "/project/fehder_718/frt_2021b/.env"
# load environmental variables
load_dotenv(dotenv_path)

# load the regions file from execucomp data
inter_path = os.getenv("INTER_DATA_DIR")
exec_path = inter_path + 'cross_gvkey2csa.dta'

exec_region = pd.read_stata(exec_path)
exec_region = exec_region[['region_code']].drop_duplicates()
exec_region_list = exec_region['region_code'].to_list()

# filter out the big regions
big_region_list = ['CS348', 'CS408', 'CS176']
exec_region_list = [x for x in exec_region_list if x not in big_region_list]

# dump files
with open('regions.json', 'w') as f:
    json.dump(exec_region_list, f)

with open('big_regions.json', 'w') as f:
    json.dump(big_region_list, f)

print("Normal Region List")
print(len(exec_region_list))
print(exec_region_list)
print("Big Region List")
print(len(big_region_list))
print(big_region_list)
print("FINISHED CREATING JSON")
"""
CREATE DATE: 10/26/2021
CREATED BY: DANIEL FEHDER
DESCRIPTION: Automated creation of regional subset files
"""
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# for now explicitely set the dotenv path. There are ways to make this slicker to not
# require an explicit reference but you need to think about execution environment and architecture
#local env path
#dotenv_path = "/Users/danielfehder/dev/frt_2021b/.env"
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

print('number of regions in data: %s'%(len(exec_region_list)))

# get the L2 data subset index
sind = sys.argv[1]

# now load the base pandas file for that subset
l2inter_path = os.getenv("L2_INTER_DIR")
l2inter_path = l2inter_path + 'combined/'
l2_file = "combine_inter_l2_match_%s.dta"%(sind)
l2_path = l2inter_path + l2_file

l2_data = pd.read_stata(l2_path)
print('Successfully Loaded L2 Data File: %s'%(l2_file))

# now loop through the region list
for region in exec_region_list:
    # get the subset of the data
    subset = l2_data[l2_data['region_code'] == '%s'%(region)]
    # now export the data
    # file name
    export_name = 'l2_region_subset_%s_%s.csv'%(region, sind)
    export_path = l2inter_path + export_name

    subset.to_csv(export_path, index=False)
    print('Successfully exported file: %s'%(export_name))

print('Finished exporting files')


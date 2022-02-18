"""
CREATE DATE: 10/26/2021
CREATED BY: DANIEL FEHDER
DESCRIPTION: Take regional subset files and combine into one regional file
"""
import pandas as pd
import os
import sys
import glob
from dotenv import load_dotenv


#local env path
#dotenv_path = "/Users/danielfehder/dev/frt_2021b/.env"
#cluster env path
dotenv_path = "/project/fehder_718/frt_2021b/.env"
# load environmental variables
load_dotenv(dotenv_path)

# load path variables

# now load the base pandas file for the subset data
l2inter_path = os.getenv("L2_INTER_DIR")
l2inter_path = l2inter_path + 'combined/'
#path for the combined regional files
output_path = os.getenv("L2_PROCESSED_DIR")

# now translate from raw index number to region code 

# get the index passed from batch and normalize to account for base diff
sind = int(sys.argv[1]) - 1

# load the regions file from execucomp data
inter_path = os.getenv("INTER_DATA_DIR")
exec_path = inter_path + 'cross_gvkey2csa.dta'

exec_region = pd.read_stata(exec_path)
exec_region = exec_region[['region_code']].drop_duplicates()
exec_region_list = exec_region['region_code'].to_list()

print('number of regions in data: %s'%(len(exec_region_list)))

# now assign the region we are zipping 
reg_code = exec_region_list[sind]
print("We are zipping this region: %s"%(reg_code))
# get the glob search path
search_path = l2inter_path + 'l2_region_subset_%s_*'%(reg_code)
print('GLOB serach path: %s'%(search_path))

all_filenames = glob.glob(search_path)
print(all_filenames)

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
# specify out_file_path
out_file_path = output_path + 'l2_region_%s.csv'%(reg_code)

combined_csv.to_csv(out_file_path, index=False)

print('Successfully wrote: %s'%(out_file_path))


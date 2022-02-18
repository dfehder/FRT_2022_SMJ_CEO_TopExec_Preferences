import pandas as pd
from dotenv import load_dotenv
import os

# for now explicitely set the dotenv path. There are ways to make this slicker to not
# require an explicit reference but you need to think about execution environment and architecture

#local
dotenv_path = "/Users/danielfehder/dev/frt_2021b/.env"
#cluster
dotenv_path = "/project/fehder_718/frt_2021b/.env"

# load environmental variables
load_dotenv(dotenv_path)

# get the path variables we need for this module
CLUSTER_BASE_DIR = os.getenv("CLUSTER_BASE_DIR")
INTER_DATA_DIR = os.getenv("INTER_DATA_DIR")
EXECUCOMP_PROCESSED_DIR = os.getenv("EXECUCOMP_PROCESSED_DIR")

# set full paths for data locations
inter_path = INTER_DATA_DIR
exec_region_path = EXECUCOMP_PROCESSED_DIR

# file names
exec_file = 'execucomp_full.dta'

exec_file_path = inter_path + exec_file


# Get full execucomp data
df = pd.read_stata(exec_file_path)
# Final dimensions 226 rows
regions = df[['region_code']]
# all distinct regions in the execucomp data
regions = regions.drop_duplicates()
# move to list for use in a loop
region_list = regions['region_code'].tolist()
# for the local version give me a subset. DELETE once moving to cluster
#region_list = region_list[:5]

# go through the regions and export seperate csv files
for region in region_list:
    rsub = df[df['region_code'] == region]
    outpath = exec_region_path + "exec_region_%s.csv"%(region)
    print(outpath)
    rsub.to_csv(outpath, index=False)
    print("finished outputting: %s"%(region))

print('Finished exporting files')


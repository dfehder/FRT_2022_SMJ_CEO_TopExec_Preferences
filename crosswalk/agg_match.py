"""
CREATE DATE: 10/29/2021
CREATED BY: DANIEL FEHDER
DESCRIPTION: Take match files and combine into one
"""
import pandas as pd
import os
import sys
import glob
from dotenv import load_dotenv


#cluster env path
dotenv_path = "/project/fehder_718/frt_2021b/.env"
# load environmental variables
load_dotenv(dotenv_path)

# Set up path vars
final_dir = os.getenv("FINAL_DATA_DIR")
match_dir = final_dir + 'matches/'

# get the glob search path
search_path = match_dir + 'matches_region_*'
print('GLOB serach path: %s'%(search_path))

# get all of the file names
all_filenames = glob.glob(search_path)
print(all_filenames)
print(len(all_filenames))
#combine all files in the list
full_exec = pd.concat([pd.read_csv(f) for f in all_filenames])

# process crosswalk
full_exec['matchcnt'] = 1

# merge in max posterior
mmax = full_exec[['execid', 'posterior']].groupby('execid').agg({'posterior':'max'})
mmax = mmax.rename(columns={'posterior':'max_pos'})
mmax = mmax.reset_index()

full_exec = full_exec.merge(mmax, how='left', on='execid', indicator=True)
print(full_exec['_merge'].value_counts())

# remove non-max matches
print("Dimension of data before max drops:%s"%(str(full_exec.shape)))
full_exec['isMax'] = full_exec.apply(lambda x: 1 if x['posterior'] == x['max_pos'] else 0, axis=1)
execs = full_exec[full_exec['isMax']>0]


# output dataset with all max matches
print("Dimension of full data:%s"%(str(execs.shape)))
print("Number of executives matched in full data: %s"%(str(execs.nunique())))
out_file_path = final_dir + 'full_matches.csv'
execs.to_csv(out_file_path, index=False)

# create final crosswalk
execs = execs.drop(columns=['isMax', '_merge'])
match_cnt = execs[['execid', 'matchcnt']].groupby('execid').agg({'matchcnt':'sum'})
match_cnt = match_cnt.reset_index()

print(match_cnt['matchcnt'].describe())

execs = execs.drop(columns=['matchcnt'])
execs = execs.merge(match_cnt, how='left', on='execid', indicator=True)
print(execs['_merge'].value_counts())
execs = execs.drop(columns=['_merge'])
execs = execs[execs['matchcnt']<5]
execs['dd'] = execs.apply(lambda x: abs(x['yob'] - int(x['dob'][-4:])), axis=1)
execs_final = execs.sort_values(['execid', 'posterior', 'dd', 'hhincome'], ascending=(True, False, True, False)).drop_duplicates(['execid'])
execs_final = execs_final.sort_values(['lalvoterid', 'posterior', 'dd', 'hhincome'], ascending=(True, False, True, False)).drop_duplicates(['lalvoterid'])

# get size info
print("Dimension of full data after non-singelton drops:%s"%(str(execs_final.shape)))
print("Number of executives matched in full data after non-singelton drops: %s"%(str(execs_final.nunique())))

# specify out_file_path
out_file_path = final_dir + 'full_matches_refined.csv'
execs_final.to_csv(out_file_path, index=False)

print('Successfully wrote: %s'%(out_file_path))

# output crosswalk for public facing website
execs_public = execs_final[['execid', 'lalvoterid', 'posterior']]
out_file_path = '/project/fehder_718/frt_2021b' + 'public_crosswalk.csv'
execs_public.to_csv(out_file_path, index=False)
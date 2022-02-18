"""
CREATE DATE: 7/9/2021
CREATED BY: DANIEL FEHDER
DESCRIPTION: Automated creation of subset files
"""
import pandas as pd
import numpy as np
import os
import sys
import l2clean
from zipfile import ZipFile
from l2datamap import DataMap
from dotenv import load_dotenv

# for now explicitely set the dotenv path. There are ways to make this slicker to not
# require an explicit reference but you need to think about execution environment and architecture
#local env path
#dotenv_path = "/Users/danielfehder/dev/frt_2021b/.env"
#cluster env path
dotenv_path = "/project/fehder_718/frt_2021b/.env"

# load environmental variables
load_dotenv(dotenv_path)


# initialization data
#dsets = ['preferences_raw', 'demographics_raw', 'match_bias']
dsets = ['l2_match']
datadictref = 'DataProcessingDictionary.xlsx'
# path of raw data files
floc = os.getenv("L2_RAW_DIR")
print("location of raw data: %s"%(floc))
# path to where processed data goes
dloc = os.getenv("L2_INTER_DIR")
print("location of processed data: %s"%(dloc))

def main():
    """Run the main script
    """
    print("filename given: %s"%(sys.argv[1]))

    # get the list of files
    states = os.listdir(floc)
    stindex = int(sys.argv[1]) - 1

    state = states[stindex][:-4]
    print('Beginning: %s \n\n\n'%(state))

    for ds in dsets:
        print('%s \n\n'%(ds))
        # instantiate the class
        datamap = DataMap(datadictref)
        # this initializes the subset data for this particular dataset
        datamap.subset(ds)
        # initializes dtype dictionary
        datamap.set_dtype()

        #import the data
        with ZipFile('%s%s.zip'%(floc,state)) as myzip:
            data = myzip.open("%s-DEMOGRAPHIC.tab"%(state))
            
        print('Successfully imported')

        df = pd.read_csv(data, sep='\t', usecols=datamap.dlist, dtype=datamap.dtyper, encoding='latin')
        
        print('Successfully put in dataframe\n')
        print('Number of rows in dataset: %s'%(len(df)))


        for var in datamap.dlist:
            print('Cleaning: %s'%(var))
            # start by getting the function that will be used for the transformation
            transfunc = datamap.clean_map[var]

            # if it is nan then ignore these variables and leave them alone
            if transfunc is np.nan:
                pass
            else:
                # variables in this part of the logic need to be changed
                # apply the right cleaning function to the data (can only be done one)
                df[var] = df[var].apply(lambda x: getattr(l2clean,transfunc)(x))

        # rename the vars so the column names don't suck
        df = df.rename(columns=datamap.rename)

        #df.to_sql(ds, conn, if_exists='append', index = False)
        df.to_pickle('%s%s_%s.pkl'%(dloc,state[5:7],ds))
        #conn.commit()
            
    print('END LOOP FOR %s \n\n'%(state))
    #conn.close()

if __name__ == "__main__":
    # run the main loop for the process
    main()

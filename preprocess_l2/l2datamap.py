"""
CREATE DATE: 7/9/2021
CREATED BY: DANIEL FEHDER
DESCRIPTION: CREATES THE DATAMAP CLASS
"""
import pandas as pd
import numpy as np

class DataMap(object):
    def __init__(self, maploc):
        self.maploc = maploc
        self.proc = pd.read_excel(maploc, sheet_name='dictionary')
        itype1 = pd.read_excel(maploc, sheet_name='proc_desc')

        # the few steps required to get the init_type dictionary
        # subset to the necessary columns for mapping
        itype = itype1[['process_type', 'init_type']]
        # set index for the right mapping dictionary
        itype = itype.set_index('process_type')
        itype = itype.to_dict()
        # now set the init_type dictionary into the class instance
        self.init_type = itype
        
        # we also need the mapping function dictionary
        # get the fields for the map
        ptype = itype1[['process_type', 'mapping_func']]
        ptype = ptype.set_index('process_type')
        ptype = ptype.to_dict()
        self.map_func = ptype


    def subset(self, dname):
        """Take the name of the data set and create the new dataset
        """
        # used to be called dlist_frame
        self.dframe = self.proc[self.proc[dname] == 1]
        self.dlist = self.dframe['Field'].to_list()
        
        # get the renaming dictionary
        names = self.dframe[['Field', 'stata_name']]
        names = names.set_index('Field')
        names = names.to_dict()
        names = names['stata_name']
        
        self.rename = names


    def set_dtype(self):
        """Creates the dictionary for the dtype option in the read_table import
        """
        # subset to necessary data and export to a records array
        dmapper = self.dframe[['Field', 'process_type']]
        dmapper = dmapper.to_records()
        # for each record array, pump it into a dictionary to be used for the import
        self.dtyper = {}
        # this will be used to determine the function used to clean the data
        self.clean_map = {}
        for record in dmapper:
            # entry 1 in the record is the first column (Field) and the second is process type
            self.dtyper[record[1]] = self.init_type['init_type'][record[2]]
            # use the same logic as above to set the final transportation function mapping
            self.clean_map[record[1]] = self.map_func['mapping_func'][record[2]]


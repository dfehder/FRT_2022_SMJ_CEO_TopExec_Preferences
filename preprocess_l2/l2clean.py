"""
CREATE DATE: 7/9/2021
CREATED BY: DANIEL FEHDER
DESCRIPTION: FUNCTIONS TO PROCESS L2 DATA TO MINIMIZE FILE SIZE
"""
import numpy as np

def yes_null(row):
    """Takes a yes/null df column and transforms it
    Arguments:
        the cell data for that column/row
    
    Returns:
        transformed data
    """
    try:
        if row == 'Yes':
            return 1
        else:
            return 0
    except TypeError:
        return 0


def is_active(row):
    """Takes a active/inactive df column and transforms it
    Arguments:
        the cell data for that column/row
    
    Returns:
        transformed data in 1/0 form
    """
    try:
        if row == 'A':
            return 1
        else:
            return 0
    except TypeError:
        return 0


def hh_gender(row):
    """Takes a household_gender df column and transforms it
    Arguments:
        the cell data for that column/row
    
    Returns:
        transformed data in 1/0 form
    """
    dispatch = {'Cannot Determine':0, 'Female Only Household':1, 
                'Male Only Household':2, 'Mixed Gender Household':3}
    try:
        for k,v in dispatch.items():
            if row == k:
                return v
            else:
                pass
            
    except KeyError:
        print(row)
        return np.nan


def hh_party(row):
    """Takes a household_gender df column and transforms it
    Arguments:
        the cell data for that column/row
    
    Returns:
        transformed data in 1/0 form
    """
    dispatch = {'Democratic':1, 'Republican':2, 
                'Independent':3, 'Democratic & Republican':12, 
                'Republican & Independent':23, 'Democratic & Independent':13, 
                'Democratic & Republican & Independent':123}
    try:
        for k,v in dispatch.items():
            if row == k:
                return v
            else:
                pass
            
    except KeyError:
        print(row)
        return np.nan


def bd_conf(row):
    """Takes a household_gender df column and transforms it
    Arguments:
        the cell data for that column/row
    
    Returns:
        transformed data in 1/2/3/4 or 0 form
    v.3.1
    """
    dispatch = {'Complete Date':1, 'Imputed based on Business Rules':2, 
                'Valid Year':3, 'Valid Year and Month or Day':4}
    try:
        for k,v in dispatch.items():
            if row == k:
                return v
            else:
                pass
            
    except KeyError:
        print(row)
        return np.nan


def ch_pty(row):
    """Takes a change_party df column and transforms it
    Arguments:
        the cell data for that column/row
    
    Returns:
        transformed data in 1/2/ or 0 form
    v.1.1
    """
    dispatch = {'Between 1 and 2 Years Ago':1, 'Between 2 and 4 Years Ago':2, 
                'Within Last 1 Year':3, 'Valid Year and Month or Day':4}
    try:
        return dispatch[str(row)]
            
    except KeyError:
        return np.nan

def gender(row):
    """Takes a gender df column and transforms it
    Arguments:
        the cell data for that column/row
    
    Returns:
        transformed data in 1/2 or 0 form
    v.1.1
    """
    dispatch = {'F':1, 'M':2}
    try:
        return dispatch[str(row)]
            
    except KeyError:
        return np.nan


def renter(row):
    """Takes a owner_renter df column and transforms it
    Arguments:
        the cell data for that column/row
    
    Returns:
        transformed data in 1/2 or 0 form
    v.1.1
    """
    dispatch = {'Likely Homeowner':1, 'Likely Renter':2}
    try:
        return dispatch[str(row)]
            
    except KeyError:
        return np.nan


def yes_unk(row):
    """Takes a owner_renter df column and transforms it
    Arguments:
        the cell data for that column/row
    
    Returns:
        transformed data in 1/2 or 0 form
    v.1.1
    """
    dispatch = {'Y':1, 'U':2}
    try:
        return dispatch[str(row)]
            
    except KeyError:
        return np.nan


def dollar(row):
    """Transforms dollar_integer type
    """
    try:
        retval = row.replace('$','')
        retval = int(retval)

        return retval

    except AttributeError:
        return np.nan


def hh_comp(row):
    """Transforms a hh_comp df column
    Arguments:
        the cell data for that column/row
    
    Returns:
        transformed data in 1/2 or 0 form
    v.1.1
    """
    dispatch = {'1 adult Female':1, '1 adult Female + Children':13, 
                '1 adult Male':2, '1 adult Male & 1 adult Female':12, 
                '1 adult Male & 1 adult Female + Children':123, '1 adult Male + Children':23, 
                '2 or more adult Females':11, '2 or more adult Females + children':113, 
                '2 or more adult Males':22, '2 or more adult Males + children':223, 'Unknown':4}
    try:
        return dispatch[str(row)]
            
    except KeyError:
        return np.nan


def marry(row):
    """Takes a owner_renter df column and transforms it
    Arguments:
        the cell data for that column/row
    
    Returns:
        transformed data in 1/2 or 0 form
    v.1.1
    """
    dispatch = {'Married':1, 'Non-Traditional':2}
    try:
        return dispatch[str(row)]
            
    except KeyError:
        return np.nan


def make_int(row):
    """Take things that should be integers and filter out
    string values
    """
    try:
        return int(row)
    except TypeError:
        print("Non-integer value error: %s"%(row))
        return np.nan
    except ValueError:
        return np.nan


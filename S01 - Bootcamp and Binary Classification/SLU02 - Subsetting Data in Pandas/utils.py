import re
import numpy as np


def duration_to_int(duration):
    """ 
    Computes integer duration of string if format corresponds to Xmin
    Args:
        str: the input duration string 
    Returns:
        int: number of corresponding minutes

    """

    match = re.match(r'(\d+ ?)(?=min)', duration)
    if match:
        return int(match.group())
    else:
        return np.nan 
    
    
def add_column_duration_int(df):
    """ 
    Add a new column to a dataframe with the duration as an integer
    Args:
        df (pd.DataFrame): the input DataFrame
    Returns:
        (pd.DataFrame): new df
    """
    
    # You will learn more about `apply` on later units
    df_new = df.copy()
    df_new['duration_int'] = df_new['duration'].apply(duration_to_int)
    return df_new

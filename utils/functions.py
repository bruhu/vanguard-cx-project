# utils/my_utils.py

import pandas as pd
import numpy as np
import re


# Reusable functions to use accross the project

# Data Inspecting

# inspect df
def inspect_dataframe(df):
    """
    Function to perform basic inspection on a DataFrame: 
    shape, column names, data types, and missing values.
    
    """

    print('Check the shape (rows, columns):')
    print(df.shape)

    print('\nColumn names:')
    print(df.columns)


    print('\nData types:')
    print(df.dtypes)


    print('\nMissing values:')
    print(df.isnull().sum())



# Data Cleaning & Data Wrangling


# clean column names
def clean_column_names(df):
    """
    Function to clean the column names of a DataFrame:
    - Convert to lowercase
    - Replace spaces with underscores
    - Remove or replace special characters with underscores

    """

    def clean_name(name):
        name = name.lower()
        name = name.replace(" ", "_")
        name = re.sub(r'[^a-z0-9_]', '_', name)
        return name
    
    df.columns = [clean_name(col) for col in df.columns]    
    return df

# check unique and empty values
def check_unique_and_empty(df):
    result = []
    
    for column in df.columns:
        unique_values = df[column].dropna().unique()
        empty_values = df[column].isna().sum()
        
        result.append({
            'Column': column,
            'Unique value count': len(unique_values),  # Number of unique values in the column
            'Empty value count': empty_values
        })
    
    result_df = pd.DataFrame(result)
    result_df.set_index('Column', inplace=True)
    
    print('Summary of Unique and Empty Values:\n')
    print(result_df)
    print('\n' + '-'*50 + '\n')


# convert floats to ints
def floats_to_ints(df, column_name):
    """
    Convert float values in the specified column to integers, leaving NaNs intact.
    This handles both NaN (from numpy) and pd.NA (from pandas' nullable integers).
    
    """
    # handle NaN and pd.NA correctly, keeping them intact
    df[column_name] = df[column_name].apply(
        lambda x: int(np.floor(x)) if pd.notna(x) and x is not pd.NA else x
    )
    
    df[column_name] = df[column_name].astype('Int64')  # 'Int64' for nullable integers in pandas
    
    return df


# handle unique values in 'gender' column
def handle_unique_gender_values(df):
    print(df['gender'].unique())
    replacement_dict_gender = {
        'U': 'Unspecified',    
        'M': 'Male',
        'F': 'Female',
        'X': 'Unspecified',
    }
    df['gender'] = df['gender'].replace(replacement_dict_gender)
    df['gender'] = df['gender'].fillna('Unspecified')
    
    return df
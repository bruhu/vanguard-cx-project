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
        'X': 'Other',
    }
    df.loc[:, 'gender'] = df['gender'].replace(replacement_dict_gender)
    df.loc[:, 'gender'] = df['gender'].fillna('Unspecified')
    
    return df


# KPI Calculations

def find_completion_rate(df):
    clients_finished = df[df['process_step'] == 4]  # filter rows where process_step is 'Finish'
    total_unique_clients = df['client_id'].nunique()
    unique_clients_finished = clients_finished['client_id'].nunique()  # find unique client ids that finished
    completion_rate = unique_clients_finished / total_unique_clients  # calculate completion rate
    print(f'Clients who finished the process: {unique_clients_finished} out ouf {total_unique_clients}.')
    return unique_clients_finished, total_unique_clients, completion_rate


def calculate_time_per_step(df):
    df = df.sort_values(by=['client_id', 'date_time'])  # sort by client_id and date_time
    df['time_diff'] = df.groupby('client_id')['date_time'].diff()  # calculate time diff between steps
    # Drop first row per client (contains no information)
    df = df.dropna(subset=['time_diff'])
    avg_time_per_step = df.groupby('process_step')['time_diff'].mean()  # calculate average time per step
    avg_time_in_seconds = avg_time_per_step.dt.total_seconds()  # convert to total seconds
    avg_time_in_seconds_rounded = np.ceil(avg_time_in_seconds).astype(int)  # round up to remove decimals
    avg_time_per_step_rounded = pd.to_timedelta(avg_time_in_seconds_rounded, unit='s')  # convert back to timedelta
    print(f'Average time spent on each step:\n {avg_time_per_step_rounded}')
    return avg_time_per_step_rounded
    

def find_error_rate(df):
    clients_with_errors = df[df['stepped_back']]['client_id'].nunique()  # unique clients who experienced at least one error
    errors_per_client = df[df['stepped_back']].groupby('client_id').size()  # errors for each client
    total_errors = df['stepped_back'].sum()  # errors across all clients
    print(f'Errors per client: {errors_per_client}')
    print(f'Total number of errors across all clients: {total_errors}')
    return clients_with_errors, errors_per_client, total_errors

def steps_to_numerical(df, column_name):
    replacement_dict_steps = {
        'start' : 0,
        'step_1' : 1,
        'step_2' : 2,
        'step_3' : 3,
        'confirm' : 4
        }
    df[column_name] = df[column_name].map(replacement_dict_steps)
    return df
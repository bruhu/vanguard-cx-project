# utils/kpi_functions.py

import pandas as pd
import numpy as np
import re

# KPI Calculations


def find_completion_rate(df):
    clients_finished = df[df['step'] == 4]  # filter rows where  is 'Finish'
    total_unique_clients = df['client_id'].nunique()
    unique_clients_finished = clients_finished['client_id'].nunique()  # find unique client ids that finished
    completion_rate = unique_clients_finished / total_unique_clients  # calculate completion rate
    print(f'Clients who finished the process: {unique_clients_finished} out ouf {total_unique_clients}.')
    return unique_clients_finished, total_unique_clients, completion_rate

def calculate_average_time_per_step(df):
    df['date_time'] = pd.to_datetime(df['date_time'])
    
    df = df.sort_values(by=['client_id', 'visit_id', 'step'])
    
    df['next_step_time'] = df.groupby(['client_id', 'visit_id'])['date_time'].shift(-1)  # Shift for next step's time
    df['time_spent'] = df['next_step_time'] - df['date_time']  # Calculate the time spent between steps
    
    step_4_rows = df[df['step'] == 4].copy()    
    step_4_rows['next_step_time'] = step_4_rows.groupby('visit_id')['date_time'].transform('max')  # Max date_time for finish
    df.loc[df['step'] == 4, 'next_step_time'] = step_4_rows['next_step_time']
    df['time_spent'] = df['next_step_time'] - df['date_time']  # Recalculate for step 4 after updating the column
    
    df = df.dropna(subset=['time_spent'])
    
    avg_time_per_step = df.groupby(['step'])['time_spent'].mean().reset_index(name='avg_time_spent')
    
    avg_time_per_step['avg_time_seconds'] = np.ceil(avg_time_per_step['avg_time_spent'].dt.total_seconds()).astype(int)
    
    avg_time_per_step['avg_time_minutes'] = avg_time_per_step['avg_time_seconds'] / 60
    
    avg_time_per_step['avg_time_minutes'] = avg_time_per_step['avg_time_minutes'].round(2)
    
    median_time = avg_time_per_step['avg_time_minutes'].median()

    print(f"Median time spent across all steps: {median_time} minutes")
    
    return avg_time_per_step
    

def find_error_rate(df):
    clients_with_errors = df[df['stepped_back']]['client_id'].nunique()  # unique clients who experienced at least one error
    errors_per_client = df[df['stepped_back']].groupby('client_id').size()  # errors for each client
    total_errors = df['stepped_back'].sum()  # errors across all clients
    print(f'Errors per client: {errors_per_client}')
    print(f'Total number of errors across all clients: {total_errors}')
    return clients_with_errors, errors_per_client, total_errors

def calculate_error_count(df):
    df = df.sort_values(by=['client_id', 'visit_id', 'date_time'])

    # backward steps (errors) for each client within each visit
    df['stepped_back'] = df.groupby(['client_id', 'visit_id'])['step'].diff() < 0

    # Calculate total errors (total backward steps)
    total_errors = df['stepped_back'].sum()

    # total steps (rows in the dataframe)
    total_steps = len(df)

    # average error count per step (percentage of steps that are errors)
    avg_error_count_per_step = df['stepped_back'].mean()  # This gives the average proportion of steps that are errors
    print(f'Average error count per step: {avg_error_count_per_step:.2f}')

    # total error count per client (sum of backward steps per client)
    total_errors_per_client = df.groupby('client_id')['stepped_back'].sum()
    print(f'Total error count per client:\n{total_errors_per_client.head()}')

    # unique clients with errors
    clients_with_errors = (total_errors_per_client > 0).sum()
    error_rate_clients = (clients_with_errors / df['client_id'].nunique()) * 100
    print(f'Error rate (clients with errors): {error_rate_clients:.2f}%')

    # percentage of total steps that have errors
    error_rate_steps = (total_errors / total_steps) * 100  # % of steps that are errors
    print(f'Error rate (steps with errors): {error_rate_steps:.2f}%')

    # error rate per step (the proportion of steps that are errors)
    df['error_rate_per_step'] = df['stepped_back'].astype(int) / 1  # each row represents a step, so this is either 0 or 1
    error_rate_per_step = df['error_rate_per_step'].mean() * 100  # mean error rate per step
    print(f'Error rate per step: {error_rate_per_step:.2f}%')

    return df, total_errors_per_client

def steps_to_numerical(df, column_name):
    step_numericals = {
        'start' : 0,
        'step_1' : 1,
        'step_2' : 2,
        'step_3' : 3,
        'confirm' : 4
        }
    df[column_name] = df[column_name].map(step_numericals)
    return df

def steps_to_text(df, column_name):
    step_names = {0: 'Start', 1: 'Step 1', 2: 'Step 2', 3: 'Step 3', 4: 'Finish'}
    df[column_name] = df[column_name].map(step_names)
    return df
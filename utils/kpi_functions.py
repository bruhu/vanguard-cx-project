# KPI Calculations

def find_completion_rate(df):
    clients_finished = df[df['step'] == 4]  # filter rows where  is 'Finish'
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
    avg_time_per_step = df.groupby('step')['time_diff'].mean()  # calculate average time per step
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
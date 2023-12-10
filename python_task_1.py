import pandas as pd

# Question 1: Car Matrix Generation
def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
     # Create a pivot table and fill NaN values with 0
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')
    car_matrix = car_matrix.fillna(0).astype(int)

    # Set diagonal values to 0
    car_matrix.values[[range(car_matrix.shape[0])]*2] = 0


    return car_matrix

    return df

# Question 2: Car Type Count Calculation
def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Create an empty dictionary to store type counts
    type_counts_dict = {'low': 0, 'medium': 0, 'high': 0}

    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        car_value = row['car']

        # Categorize 'car' values into types and update the counts
        if car_value <= 15:
            type_counts_dict['low'] += 1
        elif car_value <= 25:
            type_counts_dict['medium'] += 1
        else:
            type_counts_dict['high'] += 1

    return type_counts_dict


    return dict()

# Question 3: Bus Count Index Retrieval
def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
   # Calculate the mean of 'bus' values
    bus_mean = df['bus'].mean()

    # Create a list of indices where 'bus' values exceed twice the mean
    bus_indexes = [index for index, value in df['bus'].items() if value > 2 * bus_mean]

    return sorted(bus_indexes)

    return list()

    return list()

# Question 4: Route Filtering
def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Calculate the average 'truck' values for each route
    average_truck_values = df.groupby('route')['truck'].mean()

    # Filter routes with average 'truck' values greater than 7
    filtered_routes = sorted(route for route, avg_truck in average_truck_values.items() if avg_truck > 7)

    return filtered_routes


    return list()

# Question 5: Matrix Value Modification
def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
     # Iterate through each row and column in the DataFrame
    for row_index, row in matrix.iterrows():
        for col_index in matrix.columns:
            # Retrieve the current value
            current_value = matrix.at[row_index, col_index]

            # Check the custom conditions and modify the value accordingly
            if current_value > 20:
                matrix.at[row_index, col_index] = round(current_value * 0.75, 1)
            else:
                matrix.at[row_index, col_index] = round(current_value * 1.25, 1)

    return matrix


    return matrix

## Question 6: Time Check
def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
     # Check if the DataFrame is empty
    if df.empty:
        return pd.Series()

    # Combine 'startDay' and 'startTime' to create a start timestamp
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])

    # Combine 'endDay' and 'endTime' to create an end timestamp
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Group the DataFrame by unique (`id`, `id_2`) pairs
    grouped_data = df.groupby(['id', 'id_2'])

    # Check the completeness for each group
    completeness_check = grouped_data.apply(lambda group: (
        (group['start_timestamp'].min() == group['start_timestamp'].min().replace(hour=0, minute=0, second=0)) and
        (group['end_timestamp'].max() == group['end_timestamp'].max().replace(hour=23, minute=59, second=59)) and
        (group['end_timestamp'].max() - group['start_timestamp'].min() == pd.Timedelta(days=6, hours=23, minutes=59, seconds=59))
    ))

    return completeness_check



    return pd.Series()

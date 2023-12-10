import pandas as pd

## Question 1: Distance Matrix Calculation
def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
     # Check if the DataFrame is empty
    if df.empty:
        return pd.DataFrame()

    # Create an empty DataFrame for the distance matrix
    distance_matrix = pd.DataFrame(index=df['start'].unique(), columns=df['end'].unique())

    # Iterate through each row in the DataFrame and fill in the distance matrix
    for _, row in df.iterrows():
        start, end, distance = row['start'], row['end'], row['distance']

        # Add distance to the matrix
        distance_matrix.at[start, end] = distance
        distance_matrix.at[end, start] = distance  # Ensure symmetry

    # Fill diagonal values with 0
    distance_matrix.values[[range(distance_matrix.shape[0])]*2] = 0

    # Iterate through intermediate points to update cumulative distances
    for intermediate in distance_matrix.index:
        for start in distance_matrix.index:
            for end in distance_matrix.index:
                # Check if routes A to B and B to C are known
                if pd.notna(distance_matrix.at[start, intermediate]) and pd.notna(distance_matrix.at[intermediate, end]):
                    # Update cumulative distance A to C
                    distance_matrix.at[start, end] = distance_matrix.at[start, intermediate] + distance_matrix.at[intermediate, end]

    return distance_matrix
# Check if the DataFrame is empty
    if df.empty:
        return pd.DataFrame()

    # Create an empty DataFrame for the unrolled distances
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    # Iterate through each row and column in the distance matrix
    for start in df.index:
        for end in df.columns:
            # Skip diagonal values (same id_start and id_end)
            if start != end:
                distance = df.at[start, end]
                # Append the row to the unrolled DataFrame
                unrolled_df = unrolled_df.append({'id_start': start, 'id_end': end, 'distance': distance}, ignore_index=True)

    return unrolled_df

    return df

## Question 2: Unroll Distance Matrix
def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
   # Check if the DataFrame is empty
    if df.empty:
        return pd.DataFrame()

    # Filter DataFrame for the given reference_id
    reference_df = df[df['id_start'] == reference_id]

    # Calculate the average distance for the reference_id
    reference_avg_distance = reference_df['distance'].mean()

    # Calculate the percentage threshold
    percentage_threshold = 0.1  # 10%

    # Find IDs within the specified percentage threshold
    filtered_ids = df.groupby('id_start')['distance'].mean()
    filtered_ids = filtered_ids[(filtered_ids >= (1 - percentage_threshold) * reference_avg_distance) &
                                (filtered_ids <= (1 + percentage_threshold) * reference_avg_distance)]

    # Create a DataFrame with the filtered IDs
    result_df = pd.DataFrame({'id_start': filtered_ids.index})

    return result_df



    return df

# Question 3: Finding IDs within Percentage Threshold
def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Check if the DataFrame is empty
    if df.empty:
        return pd.DataFrame()

    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Iterate through each vehicle type and calculate toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

    return df

## Question 4: Calculate Toll Rate
def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
     # Check if the DataFrame is empty
    if df.empty:
        return pd.DataFrame()

    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Iterate through each vehicle type and calculate toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

    return df

## Question 5: Calculate Time-Based Toll Rates
def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
     # Check if the DataFrame is empty
    if df.empty:
        return pd.DataFrame()

    # Define time ranges and discount factors for weekdays and weekends
    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)),
                           (time(10, 0, 0), time(18, 0, 0)),
                           (time(18, 0, 0), time(23, 59, 59))]

    weekend_time_range = (time(0, 0, 0), time(23, 59, 59))
    weekend_discount_factor = 0.7

    # Create new columns for start and end day and time
    df['start_day'] = df['end_day'] = df['start_time'] = df['end_time'] = None

    # Iterate through each row and apply time-based toll rates
    for _, row in df.iterrows():
        # Set start and end day values
        df.at[_, 'start_day'] = row['end_day']
        df.at[_, 'end_day'] = row['end_day']

        # Check if it's a weekday or weekend
        if row['end_day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            for start_time, end_time in weekday_time_ranges:
                if start_time <= row['end_time'] <= end_time:
                    df.at[_, 'start_time'] = start_time
                    df.at[_, 'end_time'] = end_time
                    break
        elif row['end_day'] in ['Saturday', 'Sunday']:
            df.at[_, 'start_time'] = weekend_time_range[0]
            df.at[_, 'end_time'] = weekend_time_range[1]

        # Apply discount factors based on time ranges
        if row['start_time'] is not None and row['end_time'] is not None:
            if row['end_time'] <= time(10, 0, 0) or (time(18, 0, 0) <= row['end_time'] <= time(23, 59, 59)):
                df.at[_, 'moto'] *= 0.8
                df.at[_, 'car'] *= 0.8
                df.at[_, 'rv'] *= 0.8
                df.at[_, 'bus'] *= 0.8
                df.at[_, 'truck'] *= 0.8
            elif time(10, 0, 0) < row['end_time'] < time(18, 0, 0):
                df.at[_, 'moto'] *= 1.2
                df.at[_, 'car'] *= 1.2
                df.at[_, 'rv'] *= 1.2
                df.at[_, 'bus'] *= 1.2
                df.at[_, 'truck'] *= 1.2
            elif row['end_time'] <= time(23, 59, 59):
                df.at[_, 'moto'] *= 0.8
                df.at[_, 'car'] *= 0.8
                df.at[_, 'rv'] *= 0.8
                df.at[_, 'bus'] *= 0.8
                df.at[_, 'truck'] *= 0.8

    return df


    return df

import pandas as pd


def import_conflict_data(file_name):
    """
    Imports conflict data from data directory.
    And filters it based on a upper and lower bound date (datetime)

    Returns pd.DataFrame
    """

    path = f"data/{file_name}"
    # Import data
    conflict_df = pd.read_csv(path)
    conflict_df = conflict_df.reset_index(conflict_df.drop(0, inplace=True))

    # Create datetime objects
    conflict_df['date_start'] = pd.to_datetime(conflict_df['date_start'])
    conflict_df['date_end'] = pd.to_datetime(conflict_df['date_end'])

    return conflict_df

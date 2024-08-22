import pandas as pd
import numpy as np


def column_summary(
    df: pd.DataFrame,
    null_list: list = [pd.NA, np.nan, "NA", "NaN", "na", "nan", "<NA>", "N/A", "<na>"],
) -> pd.DataFrame:
    """
    This function generates a summary of a given DataFrame.

    It takes in a DataFrame and an optional list of null values,
    and returns a new DataFrame with summary information for each column.

    The summary information includes the column name, data type,
    fill percentage, number of unique values, and the most common entries.

    Parameters:
        df (pd.DataFrame): The input DataFrame to be summarized.
        null_list (list): An optional list of null values to be replaced with pd.NA.
            Defaults to [pd.NA, np.nan, "NA", "NaN", "na", "nan", "<NA>", "N/A", "<na>"].

    Returns:
        pd.DataFrame: A new DataFrame with summary information for each column.
    """
    # if df is empty, return an empty dataframe with just the column names
    if df.empty:
        return pd.DataFrame(
            columns=[
                "Column",
                "Data Type",
                "Fill Percentage",
                "Unique Values",
                "Most Common Entries",
            ]
        )
    else:
        df = df.reset_index()
        col_list = []
        # Loop through the columns in the DataFrame
        for column_name in df.columns:
            # Get the data type of the column
            dtype = df[column_name].dtype

            # Replace values in the column_name that are in the null_list with pd.NA
            df[column_name] = df[column_name].mask(
                df[column_name].isin(null_list), pd.NA
            )

            # Get the fill percentage of the column
            fill_percentage = df[column_name].count() / len(df) * 100

            # Get the most common entries in the column
            most_common_entries = "; ".join(
                df[column_name].astype(str).value_counts().head(5).index.to_list()
            )

            # Create a row for the summary DataFrame
            row = pd.Series(
                {
                    "Column": column_name,
                    "Data Type": dtype,
                    "Fill Percentage": fill_percentage,
                    "Unique Values": df[column_name].nunique(),
                    "Most Common Entries": most_common_entries,
                }
            )

            # Append the row to the summary DataFrame
            col_list.append(row)

        summary_df = pd.DataFrame(col_list)

        # Return the summary DataFrame
        return summary_df

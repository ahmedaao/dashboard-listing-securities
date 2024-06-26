"""This module contains functions which aggregate by attribute"""
import pandas as pd


def sum_by_attribute(attribute: str, dict_attribute: dict) -> dict:
    """
    Group a dictionary by a specified attribute and sum the 'quantity' for each group.

    Parameters:
    attribute (str): The key of the dictionary to group by.
    dict_attribute (dict): The dictionary containing the data.
                           It should have at least the keys specified by `attribute` and 'quantity'.

    Returns:
    dict: A dictionary where the keys are the unique values of the specified attribute 
          and the values are the sum of the 'quantity' for each group.
    """
    # Convert the dictionary to a pandas DataFrame
    df_attribute = pd.DataFrame(dict_attribute)
    # Group the DataFrame by the specified attribute and sum the 'quantity' for each group
    groupby_attribute = df_attribute.groupby(attribute)['quantity'].sum().reset_index()
    # Convert the resulting DataFrame back to a dictionary with lists as values
    result = groupby_attribute.to_dict(orient='list')

    return result

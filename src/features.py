"""Module containing functions to add features"""

import pandas as pd


def add_column_total(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add column "Total" which is the sum of Quantity and Unit_price.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
    """
    # Feature1: Total amount for a transaction
    df["total"] = df["quantity"] * df["unitPrice"]

    return df

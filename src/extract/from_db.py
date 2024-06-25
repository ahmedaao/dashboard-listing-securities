"""This module contains functions which extract data from sqlite database.db"""
import sqlite3
from sqlite3 import Error


def connection_to(db_file: str):
    """ Create a connection to the SQLite database specified by db_file. """
    try:
        conn = sqlite3.connect(db_file)
        print(f"Successfully connected to {db_file}")
        return conn
    except Error as e:
        print(f"Error connecting to {db_file}: {e}")
        return None


def by_attribute(db_file: str, attribute: str) -> dict:
    """
    Extract the values of a specified attribute from the transaction table and organize them into a dictionary.

    :param db_file (str): Path to the SQLite database file
    :param attribute (str): Name of the attribute to extract
    :return: Dictionary with key=(date, quantity, unitPrice) and values of the specified attribute in list form
    """
    conn = connection_to(db_file)
    if conn is None:
        return {}

    try:
        cursor = conn.cursor()

        joins = {
            "isinId": "JOIN isin ON 'transaction'.isinId = isin.id",
            "brokerId": "JOIN broker ON 'transaction'.brokerId = broker.id",
            "accountId": "JOIN account ON 'transaction'.accountId = account.id",
            "orderId": "JOIN 'order' ON 'transaction'.orderId = 'order'.id",  # 'order' is a reserved keyword, use quotes
        }

        columns = {
            "isinId": "isin, name, type",
            "brokerId": "name, country",
            "accountId": "number, name",
            "orderId": "id, type"
        }

        if attribute in joins and attribute in columns:
            query = (
                f"SELECT 'transaction'.date, "
                f"{columns[attribute]}, "
                f"'transaction'.quantity, 'transaction'.unitPrice, "
                f"('transaction'.quantity * 'transaction'.unitPrice) AS total "
                f"FROM 'transaction' "
                f"{joins[attribute]};"
            )
        else:
            print(f"Attribute '{attribute}' not recognized for join.")
            return {}

        cursor.execute(query)
        rows = cursor.fetchall()

        # Define the keys for the dictionary using original attribute names
        keys = ['date'] + [col.split(' ')[-1] for col in columns[attribute].split(', ')] + ['quantity', 'unitPrice', 'total']

        # Initialize the result dictionary with empty lists
        result = {key: [] for key in keys}

        # Populate the result dictionary
        for row in rows:
            for key, value in zip(keys, row):
                result[key].append(value)

        return result
    except Error as e:
        print(f"Error extracting data: {e}")
        return {}
    finally:
        if conn:
            conn.close()


def all_attributes(db_file: str) -> dict:
    """
    Connect to the SQLite database and merge all specified tables into a single result set.

    :param db_file (str): Path to the SQLite database file
    :return: List of dictionaries representing the merged result set.
    """
    conn = connection_to(db_file)
    if conn is None:
        return {}

    try:
        cursor = conn.cursor()

        # Define the SQL query to join all tables
        query = """
        SELECT
            'transaction'.date,
            isin.isin, isin.name, isin.type,
            broker.name, broker.country,
            account.number, account.name,
            'order'.type,
            'transaction'.quantity, 'transaction'.unitPrice,
            ('transaction'.quantity * 'transaction'.unitPrice) AS total
        FROM
            'transaction'
        JOIN isin ON 'transaction'.isinId = isin.id
        JOIN broker ON 'transaction'.brokerId = broker.id
        JOIN account ON 'transaction'.accountId = account.id
        JOIN 'order' ON 'transaction'.orderId = 'order'.id;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        # Define the keys for the dictionary using original attribute names
        keys = [
            'date',
            'isin', 'isin_name', 'isin_type',
            'broker_name', 'broker_country',
            'account_number', 'account_name',
            'order_type',
            'quantity', 'unitPrice',
            'total'
        ]

        # Initialize the result dictionary with empty lists
        result = {key: [] for key in keys}

        # Populate the result dictionary
        for row in rows:
            for key, value in zip(keys, row):
                result[key].append(value)

        return result
    except Error as e:
        print(f"Error extracting data: {e}")
        return {}
    finally:
        if conn:
            conn.close()

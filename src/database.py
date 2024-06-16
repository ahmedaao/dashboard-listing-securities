"""This module contains functions which realize CRUD operations"""

import sqlite3
import pandas as pd


def create_from_csv(csv_file: str, database_file: str):
    """
    Create a SQLite database and populate it with data from a CSV file.

    This function reads data from a specified CSV file and inserts it into
    a SQLite database. It creates five tables: account, broker, order, security,
    and transaction. The transaction table uses foreign keys that reference the
    other tables.

    Parameters:
    csv_file (str): The path to the CSV file containing the transaction data.

    The CSV file should have the following columns:
    id, isinId, brokerId, accountId, date, orderId, quantity, unitPrice
    """

    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Create tables if they don't already exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "account" (
            id INTEGER PRIMARY KEY,
            number TEXT,
            name TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "broker" (
            id INTEGER PRIMARY KEY,
            name TEXT,
            country TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "order" (
            id INTEGER PRIMARY KEY,
            type TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "security" (
            id INTEGER PRIMARY KEY,
            isin TEXT,
            name TEXT,
            type TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "transaction" (
            id INTEGER PRIMARY KEY,
            isinId INTEGER,
            brokerId INTEGER,
            accountId INTEGER,
            orderId INTEGER,
            date TEXT,
            quantity REAL,
            unitPrice REAL,
            FOREIGN KEY (isinId) REFERENCES security (id),
            FOREIGN KEY (brokerId) REFERENCES broker (id),
            FOREIGN KEY (accountId) REFERENCES account (id),
            FOREIGN KEY (orderId) REFERENCES "order" (id)
        )
    """
    )

    # Insert fixed data into account, broker, order, and security tables
    cursor.execute(
        """
        INSERT OR IGNORE INTO "account" (id, number, name) VALUES
        (1, '508TI00083440250EUR', 'PEA'),
        (2, '508TI00084026141EUR', 'PEA-PME'),
        (3, '0422720001', 'CTO')
    """
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO "broker" (id, name, country) VALUES
        (1, 'BourseDirect', 'FRANCE'),
        (2, 'TradeRepublic', 'GERMANY')
    """
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO "order" (id, type) VALUES
        (1, 'SELL'),
        (2, 'BUY')
    """
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO "security" (id, isin, name, type) VALUES
        (1, 'LU0131510165', 'Independance et Expansion France Small A', 'OPVCM'),
        (2, 'LU1964632324', 'Independance et Expansion France Small I', 'OPVCM'),
        (3, 'LU1832174962', 'Independance et Expansion Europe Small A', 'OPVCM'),
        (4, 'LU1832175001', 'Independance et Expansion Europe Small I', 'OPVCM'),
        (5, 'US0846707026', 'Berkshire Hathaway Inc.', 'STOCK'),
        (6, 'LU1832175001', 'Markel Group Inc.', 'STOCK')
    """
    )

    # Insert data from the CSV file into the transaction table
    for row in df.itertuples(index=False):
        cursor.execute(
            """
            INSERT INTO "transaction" (id, isinId, brokerId, accountId, orderId, date, quantity, unitPrice)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                row.id,
                row.isinId,
                row.brokerId,
                row.accountId,
                row.orderId,
                row.date,
                row.quantity,
                row.unitPrice,
            ),
        )

    # Commit the transactions and close the connection
    conn.commit()
    conn.close()


def list_tables(database_file: str) -> list:
    """
    List all tables in the given SQLite database.

    This function connects to the specified SQLite database file,
    retrieves the names of all tables, and returns them as a list.

    Parameters:
    database_file (str): The path to the SQLite database file.

    Returns:
    list: A list of table names in the database.
    """

    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Execute the command to retrieve the names of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # Fetch the results
    tables = cursor.fetchall()

    # Close the connection to the database
    conn.close()

    # Extract the table names from the results and return them as a list
    return [table[0] for table in tables]

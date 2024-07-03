#!/usr/bin/env python3
"""
Module for filtering Personally Identifiable Information (PII) in logs.
"""
import logging
import os
import re
from typing import List

import mysql.connector
from mysql.connector.cursor import MySQLCursorDict

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Obfuscates PII fields in a log message.

    Args:
        fields (List[str]): List of PII fields to obfuscate.
        redaction (str): The string to replace PII fields with.
        message (str): The log message containing PII.
        separator (str): The separator used in the log message.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(
            f"{field}=.+?{separator}",
            f"{field}={redaction}{separator}",
            message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for obfuscating PII in logs.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter.

        Args:
            fields (List[str]): List of PII fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, obfuscating PII fields.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            str: The formatted log record with obfuscated PII fields.
        """
        original_message = logging.Formatter.format(self, record)
        filtered_message = filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR
        )
        if not filtered_message.endswith(self.SEPARATOR):
            filtered_message += self.SEPARATOR
        return filtered_message


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger for user data with PII redaction.

    Returns:
        logging.Logger: Configured logger with redaction formatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database
    (mysql.connector.connection.MySQLConnection object).

    You will connect to a secure holberton database to read a users table.
    The database is protected by a username and password that are set as
    environment variables on the server named PERSONAL_DATA_DB_USERNAME,
    (set the default as “root”), PERSONAL_DATA_DB_PASSWORD (set the default
    as an empty string) and PERSONAL_DATA_DB_HOST (set the default as
    “localhost”).
    The database name is stored in PERSONAL_DATA_DB_NAME.

    Returns:
        mysql.connector.connection.MySQLConnection: Connector to the
        database.
    """
    # Get the environment variables for the database credentials
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    #  OR db_name = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    # Connect to the database using the obtained credentials
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


# def get_db() -> mysql.connector.connection.MySQLConnection:
#     """
#     Establishes a connection to the database.

#     Returns:
#         Database connection object.
#     """
#     connection = mysql.connector.connection.MySQLConnection(
#         user=environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
#         password=environ.get("PERSONAL_DATA_DB_PASSWORD", ""),
#         host=environ.get("PERSONAL_DATA_DB_HOST", "localhost"),
#         database=environ.get("PERSONAL_DATA_DB_NAME"),
#         port=3306
#     )

#     return connection


def main() -> None:
    """
    Obtain a database connection using get_db and retrieve all rows
    in the users table and display each row under a filtered format
    """
    db_connection = get_db()
    cursor: MySQLCursorDict = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in cursor:
        log_message = "; ".join(f"{key}={value}" for key, value in row.items())
        logger.info(log_message)

    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()

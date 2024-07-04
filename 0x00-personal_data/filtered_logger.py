#!/usr/bin/env python3
"""
This module contains functionality for filtering Personally Identifiable
Information (PII) in logs and connecting to a MySQL database to retrieve
and log user data.
"""

import logging
import re
from os import getenv
from typing import List

import mysql.connector

PII_FIELDS = ("ssn", "password", "name", "email", "phone")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Returns the log message obfuscated.

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
            f"{field}=(.+?){separator}",
            f"{field}={redaction}{separator}",
            message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class for obfuscating PII in logs."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter.

        Args:
            fields (List[str]): List of PII fields to obfuscate.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, obfuscating PII fields.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            str: The formatted log record with obfuscated PII fields.
        """
        original_message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR
        )


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
    """
    Establishes a connection to the database.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object.
    """
    username = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database_name = getenv("PERSONAL_DATA_DB_NAME")

    if not database_name:
        raise ValueError("No database name provided")

    connection = mysql.connector.connect(
        host=host, user=username, password=password, database=database_name
    )

    return connection


def main() -> None:
    """
    Main function to retrieve all rows in the users table and display each
    row under a filtered format.
    """
    logger = get_logger()
    db_connection = get_db()

    cursor = db_connection.cursor()
    cursor.execute("DESCRIBE users;")
    headers = [row[0] for row in cursor.fetchall()]
    cursor.close()

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users;")

    for row in cursor.fetchall():
        message = (
            "; ".join(f"{header}={value}" for header,
                      value in zip(headers, row)) + ";"
        )
        logger.info(message)

    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()

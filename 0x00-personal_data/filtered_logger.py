#!/usr/bin/env python3
"""
Provide functions to process log messages
"""
import re
import typing as t
import logging
import mysql.connector
from os import getenv

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: t.List[str]):
        """
        Initialization method
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log message
        """
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


def filter_datum(
    fields: t.List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    Obfuscate log message
    """
    regex = r'(?P<field>{})=[^{}]*'.format('|'.join(fields), separator)
    return re.sub(regex, r'\g<field>={}'.format(redaction), message)


def get_logger() -> logging.Logger:
    """
    Get a logger instance
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Get a database connection
    """
    db_host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )

    return connection


def main() -> None:
    """
    Fetch users from a db, and display user details
    """
    fields = 'name,email,phone,ssn,password,ip,last_login,user_agent'
    fields = fields.split(',')

    logger = get_logger()
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users;")
        for row in cursor:
            record = map(
                lambda x: "{}={}".format(x[0], x[1]),
                zip(fields, row),
            )
            msg = "{};".format('; '.join(list(record)))
            logger.info(msg)


if __name__ == '__main__':
    main()

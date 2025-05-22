#!/usr/bin/env python3
'''Function filter_datum'''
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    '''Function that returns the log message obfuscated'''
    reg = rf'({"|".join(map(re.escape, fields))})=([^{re.escape(separator)}]+)'
    final = re.sub(reg, lambda x: f'{x.group(1)}={redaction}', message)
    return final


def get_logger() -> logging.Logger:
    '''Function that returns a logging.Logger object.'''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''function that returns a connector to the database'''
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', "root")
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', "")
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', "localhost")
    db_name = os.getenv('PERSONAL_DATA_DB_NAME', "")
    db_connect = mysql.connector.connect(
        user=username,
        password=password,
        host=db_host,
        database=db_name
    )
    return db_connect


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''instantiation'''
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        '''filter values of formatted records'''
        formatted = super(RedactingFormatter, self).format(record)
        new_message = filter_datum(self.fields,
                                   self.REDACTION,
                                   formatted,
                                   self.SEPARATOR)
        return new_message


def main() -> None:
    '''main Function'''
    db = get_db()
    cursor = db.cursor()
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    cursor.execute("SELECT {} from users;".format(fields))
    logger = get_logger()
    rows = cursor.fetchall()
    for row in rows:
        record = [f'{field}={value}' for field, value in zip(columns, row)]
        message = ';'.join(record) + ';'
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()

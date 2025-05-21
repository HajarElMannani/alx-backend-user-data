#!/usr/bin/env python3
'''Function filter_datum'''
from typing import List
import re
import logging


PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')


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

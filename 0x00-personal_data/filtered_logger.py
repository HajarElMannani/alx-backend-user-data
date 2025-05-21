#!/usr/bin/env python3
'''Function filter_datum'''
from typing import List
import re
import logging


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    '''Function that returns the log message obfuscated'''
    reg = rf'({"|".join(map(re.escape, fields))})=([^{separator}]+)'
    final = re.sub(reg, lambda x: f'{x.group(1)}={redaction}', message)
    return final


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[ALX] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields) -> None:
        '''instantiation'''
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        '''filter values of formatted records'''
        formatter = logging.Formatter(RedactingFormatter.FORMAT)
        formatted = formatter.format(record)
        new_message = filter_datum(self.fields,
                                   RedactingFormatter.REDACTION,
                                   formatted,
                                   RedactingFormatter.SEPARATOR)
        return new_message

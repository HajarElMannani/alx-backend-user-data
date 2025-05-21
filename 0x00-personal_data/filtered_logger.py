#!/usr/bin/env python3
'''Function filter_datum'''
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    '''Function that returns the log message obfuscated'''
    reg = rf'({"|".join(map(re.escape, fields))})=([^{separator}]+)'
    final = re.sub(reg, lambda x: f'{x.group(1)}={redaction}', message)
    return final

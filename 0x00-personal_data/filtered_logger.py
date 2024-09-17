#!/usr/bin/env python3
"""
Provide functions to process log messages
"""
import re
import typing as t


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

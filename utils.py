# -*- coding: utf-8 -*-

from configparser import ConfigParser
import csv
import os


def csvfile(file_name):
    result = []
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) == 1:
                result.append(row[0])
            else:
                result.append(row)
    return result


def get_variable(variable_name, default_value):
    if variable_name in os.environ:
        return os.environ[variable_name]
    else:
        return default_value


def read_variable(file_name, variable_name):
    parser = ConfigParser()
    try:
        with open(file_name) as lines:
            lines = chain(("[top]",), lines)
            parser.read_file(lines)
        return parser['top'][variable_name]
    except IOError as ex:
        raise ImproperlyConfigured(f'File could not be read: {file_name}')
    except KeyError as ex:
        raise ImproperlyConfigured(f'Variable not found: {variable_name}')


def read_or_get(file_name, variable_name, default_value):
    return read_variable(file_name, variable_name) or get_variable(variable_name, default_value)

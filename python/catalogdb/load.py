#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2019-07-26
# @Filename: load.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)
#
# @Last modified by: José Sánchez-Gallego (gallegoj@uw.edu)
# @Last modified time: 2019-07-28 20:03:11

import gzip
import os
import re

import psycopg2


def get_connection(database, user, host='localhost', port=5432):
    """Returns a psycopg2 database connection."""

    conn = psycopg2.connect(f'dbname={database} user={user} host={host} port={port}')

    return conn


def read_table_definition(fn):
    """Reads a table definition file.

    The file must contain one line per column in the new table with format ::

        COLUMN_NAME TYPE [EXTRA_PARAMETERS]

    Lines starting with ``#`` are ignored.

    Parameters
    ----------
    fn : str
        The path to the file with the table definition.

    Returns
    -------
    table_definition : list
        A list of columns in PostgreSQL format.

    """

    columns = []

    assert os.path.exists(fn), 'file does not exist.'

    with open(fn) as unit:

        for line in unit.read().splitlines():
            stripped = line.strip()
            if stripped.startswith('#'):
                continue
            stripped = re.sub(r'\[|\]', '', stripped)
            columns.append(stripped)

    return columns


def table_exists(conn, table_name, schema=False):
    """Checks if a table exists.

    Parameters
    ----------
    conn
        A Psycopg2 connection.
    table_name : str
        The table name.
    schema : str
        The schema to which the table belongs.

    """

    cur = conn.cursor()

    table_exists_sql = ('select * from information_schema.tables '
                        f'where table_name={table_name!r}')

    if schema:
        table_exists_sql += f' and table_schema={schema!r}'

    cur.execute(table_exists_sql)

    return bool(cur.rowcount)


def copy_csv(conn, table_name, file, schema=None, header=False, sep=','):
    """Copies a CSV file to a table. Supports gzipped files.

    Parameters
    ----------
    conn
        A Psycopg2 connection.
    table_name : str
        The table name.
    file : str
        The CSV file to copy. Can be compressed using gzip.
    schema : str
        The schema to which the table belongs.
    header : bool
        Whether the file contains a header in the first line.
    sep : str
        The separator between column values.

    Returns
    -------
    result : bool
        `True` if the copy was successfull, `False` otherwise.
    """

    full_table_name = f'{schema}.{table_name}' if schema else table_name

    if isinstance(conn, dict):
        conn = get_connection(conn['dbname'], conn['user'],
                              conn['host'], conn['port'])

    if not table_exists(conn, table_name, schema):
        return False

    is_gzip = False
    with open(file, 'rb') as funit:
        if funit.read(2) == b'\x1f\x8b':  # All gzip files start with 1F 8B
            is_gzip = True

    fobj = open(file, 'r') if not is_gzip else gzip.GzipFile(file)

    # Skips the header
    if header:
        next(fobj)

    cursor = conn.cursor()

    copy_sql = f'COPY {full_table_name} FROM STDOUT WITH CSV DELIMITER {sep!r}'
    cursor.copy_expert(copy_sql, fobj)

    conn.commit()
    conn.close()

    return True

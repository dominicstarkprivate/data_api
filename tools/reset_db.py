#!/usr/bin/env python
"""This script resets the database, i.e. it deletes any old data (if there is
any) and creates an empty database. Note that this script is meant to be called
from the Makefile, hence it assumes that it is called from the root of the
directory.
"""
import sqlite3

# Set up connection to a database. This creates a db file at the given
# position, if it doesn't exist yet.
connection = sqlite3.connect("./customer_texts.db")

# Open the schema file and execute it. This deletes any data that is
# currently saved in the database (if one exists).
with open("./schema.sql") as f:
    connection.executescript(f.read())

# Commit and close.
connection.commit()
connection.close()

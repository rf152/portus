#!/usr/bin/env python

import sqlite3;
import log;
import config;

connection = None;
cursor = None;
logger = None;

def load_schema(filename='/opt/portus/share/schema.sql'):
	with open(filename, 'r') as fh:
		contents = fh.read();
	logger.debug("Loading Schema");
	cursor.executescript(contents);
	connection.commit();


# Init stuff
if logger == None:
	logger = log.get(__name__);
logger.debug("Database starting up");
dbfile = config.get('db', 'filename');

if connection == None:
	connection = sqlite3.connect(dbfile);
if cursor == None:
	cursor = connection.cursor();



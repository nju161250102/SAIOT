# -*- coding=utf-8 -*-
"""
Under the same directory use

'python CreateSAIOTDB.py'

to generate original sqlite db for this project
"""
import sqlite3


conn = sqlite3.connect('saiot.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS device;")
c.execute('''
CREATE TABLE device (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  name TEXT DEFAULT NULL,
  dcode TEXT DEFAULT NULL,
  secret TEXT DEFAULT NULL,
  type TEXT DEFAULT NULL,
  ip TEXT DEFAULT NULL,
  port INTEGER DEFAULT NULL,
  description TEXT DEFAULT NULL);
''')

c.execute("DROP TABLE IF EXISTS connection;")
c.execute('''
CREATE TABLE connection (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  deviceId INTEGER NOT NULL,
  topic TEXT DEFAULT NULL);
''')

c.execute("DROP TABLE IF EXISTS rule;")
c.execute('''
CREATE TABLE rule (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  name TEXT DEFAULT NULL,
  description TEXT DEFAULT NULL,
  deviceId INTEGER NOT NULL,
  topic TEXT DEFAULT NULL,
  columns TEXT DEFAULT NULL,
  condition TEXT DEFAULT NULL,
  path TEXT DEFAULT NULL,
  status INTEGER DEFAULT 0);
''')

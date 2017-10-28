#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: toddler
# date: 20171026

# 数据库使用sqlite, ORM使用sqlalchemy

import sqlite3
import sys

sys.path.append("..")
from Lib.my_lib import WriteLog, re_joint_dir_by_os

db_path = re_joint_dir_by_os('..|Data|analyzeCoding.db')

db = sqlite3.connect(db_path)
cur = db.cursor()

create_sql = """
                    CREATE TABLE IF NOT EXISTS coding_all_user (
                              ID INTEGER PRIMARY KEY AUTOINCREMENT,
                              global_key VARCHAR NOT NULL,
                              friends VARCHAR NOT NULL
                            )
"""

cur.execute(create_sql)

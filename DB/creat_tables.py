#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: toddler
# date: 20171026

# 数据库使用sqlite, ORM使用sqlalchemy

import sqlite3
import sys
import os

sys.path.append("..")
from Lib.my_lib import WriteLog, re_joint_dir_by_os
from Conf.analyzecoding import db_path

db_path = os.path.join(os.path.abspath(".."), re_joint_dir_by_os(db_path))


def create_coding_all_user():
    db = sqlite3.connect(db_path)
    cur = db.cursor()
    create_sql = """
                        CREATE TABLE IF NOT EXISTS coding_all_user (
                                  ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                  global_key VARCHAR NOT NULL,
                                  friends_count INTEGER NOT NULL,
                                  friends VARCHAR NOT NULL
                                )
    """
    cur.execute(create_sql)
    db.close()


if __name__ == '__main__':
    create_coding_all_user()

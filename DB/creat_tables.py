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
                                  global_key VARCHAR PRIMARY KEY NOT NULL,
                                  friends_count INTEGER,
                                  friends VARCHAR,
                                  followers_count INTEGER,
                                  followers VARCHAR
                                )
    """

    cur.execute(create_sql)
    db.close()


def create_coding_user_info():
    db = sqlite3.connect(db_path)
    cur = db.cursor()
    create_sql = """
                        CREATE TABLE IF NOT EXISTS coding_user_info (
                                  global_key VARCHAR PRIMARY KEY NOT NULL,
                                  user_name VARCHAR,
                                  name_pinyin VARCHAR,
                                  sex VARCHAR,
                                  slogan VARCHAR,
                                  company VARCHAR,
                                  job VARCHAR,
                                  tags VARCHAR,
                                  skills VARCHAR,
                                  website VARCHAR,
                                  introduction VARCHAR,
                                  avatar VARCHAR,
                                  school VARCHAR,
                                  follows_count VARCHAR,
                                  fans_count INTEGER,
                                  tweets_count INTEGER,
                                  vip VARCHAR,
                                  created_at VARCHAR,
                                  last_logined_at VARCHAR,
                                  last_activity_at VARCHAR
                                )
    """
    cur.execute(create_sql)
    db.close()


if __name__ == '__main__':
    create_coding_all_user()
    create_coding_user_info()

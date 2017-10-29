#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: toddler

# 分析用户之前的关注关系

import sqlite3
import sys
import networkx
import matplotlib.pyplot as plt

sys.path.append("..")
from Lib.my_lib import WriteLog, re_joint_dir_by_os

wl = WriteLog(re_joint_dir_by_os("..|Logs|user_relation.log"))

db_path = re_joint_dir_by_os('..|Data|analyzecoding.db')
db = sqlite3.connect(db_path)
cur = db.cursor()

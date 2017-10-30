#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: toddler
# update: 20171029

import sys
import sqlite3

sys.path.append("..")
from Lib.my_lib import WriteLog, re_joint_dir_by_os, load_user_agents


db_path = re_joint_dir_by_os('..|Data|analyzecoding.db')
db = sqlite3.connect(db_path)
cur = db.cursor()

cur.execute("SELECT global_key FROM coding_all_user")
all_users = cur.fetchall()

users = list()
for u in all_users:
    users.append(u[0])

cur.execute("SELECT friends FROM coding_all_user")
all_friends = cur.fetchall()

friends = list()
for fr in all_friends:
    friends.extend(fr[0].split(','))

cur.execute("SELECT followers FROM coding_all_user")
all_followers = cur.fetchall()

followers = list()
for fo in all_followers:
    followers.extend(fo[0].split(','))


print len(users)
print len(friends)
print len(followers)

set_users = set(users)
set_friends = set(friends)
set_followers = set(followers)

# print 'user_friends', len(set_users - set_friends), set_users - set_friends
# print 'user_followers', len(set_users - set_followers), set_users - set_followers

print 'friends_users', len(set_friends - set_users), set_friends - set_users
print 'followers_users', len(set_followers - set_users), set_followers - set_users

# print 'friends_followers', len(set_friends - set_followers), set_friends - set_followers
# print 'followers_friends', len(set_followers - set_friends), set_followers - set_friends
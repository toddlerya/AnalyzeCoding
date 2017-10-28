#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: toddler

import requests
import sys
import sqlite3
from collections import deque

sys.path.append("..")
from Lib.my_lib import WriteLog, re_joint_dir_by_os, load_user_agents

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br"
}

ua_file = re_joint_dir_by_os('user_agents.txt')
ua_list = load_user_agents(ua_file)


db_path = re_joint_dir_by_os('..|Data|test.db')
db = sqlite3.connect(db_path)
cur = db.cursor()
insert_sql = "INSERT INTO coding_all_user (global_key, friends) VALUES (?, ?)"


def crawl_best_user():
    """
    获取热门用户作为种子
    :return:
    """
    url_best_user = "https://coding.net/api/tweet/best_user"
    bu_resp = requests.get(url_best_user, headers=headers)
    if bu_resp.status_code != 200:
        print '无法访问热门用户URL'
        sys.exit()
    else:
        try:
            seeds = list()
            temp_json_data = bu_resp.json()
            if temp_json_data['code'] == 0:
                users_data = temp_json_data['data']
                for user in users_data:
                    global_key = user['global_key']
                    if global_key != 'coding':
                        seeds.append(global_key)
                return seeds
            else:
                print "获取热门用户信息异常, json状态码不为0"
                return False
        except requests.RequestException as err:
            raise err


def crawl_user_friends(father_nodes):
    """
    获取用户关注人列表
    :param global_keys 父节点列表
    :return:
    """
    payload = {
        'page': '1',
        'pageSize': '999999999'
    }
    for global_key in father_nodes:
        each_user_friends = ['coding']  # 初始化一个共有用户, 此用户无friends_api与followers_api
        friends_api = 'https://coding.net/api/user/friends/{0}'.format(global_key)
        print friends_api
        fr = requests.get(friends_api, params=payload)
        if fr.status_code == 200:
            f_json = fr.json()
            if f_json['code'] == 0:
                user_friends_info = f_json['data']['list']
                for fi in user_friends_info:
                    friend = fi['global_key']
                    if friend not in each_user_friends:
                        each_user_friends.append(friend)
                user_all_friends = ','.join(each_user_friends)
                cur.execute(insert_sql, (global_key, user_all_friends))
                db.commit()
                each_user_friends.remove('coding')
                crawl_user_friends(each_user_friends)
            else:
                print f_json['code']
        else:
            print fr.status_code


def crawl_user_followers(global_key):
    """
    获取用户的粉丝列表
    :param global_key 用户的全局唯一标识
    :return:
    """
    followers_api = 'https://coding.net/api/user/followers/{}?page=1&pageSize=999999999'.format(global_key)



def main():
    seed_users = crawl_best_user()
    print seed_users
    # if seed_users:
    #     crawl_user_friends(seed_users)
    # else:
    #     print '未获取到第一个用户信息'
    #     sys.exit()
    # f_all_user.close()
    # db.close()


if __name__ == '__main__':
    main()
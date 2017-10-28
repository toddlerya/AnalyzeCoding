#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: toddler

import requests
import sys
import sqlite3
import os

sys.path.append("..")
from Lib.my_lib import WriteLog, re_joint_dir_by_os, load_user_agents

sys.setrecursionlimit(999999999)  # 设置递归深度, 避免报错 RuntimeError: maximum recursion depth exceeded in cmp

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br"
}

ua_file = os.path.abspath('user_agents.txt')
ua_list = load_user_agents(ua_file)

wl = WriteLog(re_joint_dir_by_os("..|Logs|crawl_all_user.log"))

db_path = re_joint_dir_by_os('..|Data|analyzecoding.db')
db = sqlite3.connect(db_path)
cur = db.cursor()
insert_sql = "INSERT INTO coding_all_user (global_key, friends_count, friends) VALUES (?, ?, ?)"

cur.execute("SELECT global_key FROM coding_all_user")
temp_query_db_users = cur.fetchall()
if len(temp_query_db_users) > 0:
    db_users = [item[0] for item in temp_query_db_users]
    all_user_list = db_users
else:
    all_user_list = ['coding']  # 初始化一个共有用户, 此用户无friends_api与followers_api


def crawl_best_user():
    """
    获取热门用户作为种子
    :return:
    """
    url_best_user = "https://coding.net/api/tweet/best_user"
    bu_resp = requests.get(url_best_user, headers=headers)
    if bu_resp.status_code != 200:
        wl.wl_error('无法访问热门用户URL: {}'.format(url_best_user))
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
                wl.wl_error("获取热门用户信息异常, json状态码不为0")
                return False
        except requests.RequestException as err:
            wl.wl_error("requests报错: {}".format(err))
            raise err


def crawl_user_friends(father_nodes):
    """
    获取用户关注人列表
    :param father_nodes 父节点列表
    :return:
    """
    payload = {
        'page': '1',
        'pageSize': '999999999'
    }
    for global_key in father_nodes:
        each_user_friends = list()
        if global_key in all_user_list:
            continue
        try:
            friends_api = 'https://coding.net/api/user/friends/{0}'.format(global_key.encode('utf-8'))
        except Exception, url_api_err:
            wl.wl_error("拼接获取朋友API-URL错误: {}".format(url_api_err))
            wl.wl_info("当前爬取URL: {}".format(friends_api))
        fr = requests.get(friends_api, params=payload)
        if fr.status_code == 200:
            f_json = fr.json()
            if f_json['code'] == 0:
                user_friends_info = f_json['data']['list']
                for fi in user_friends_info:
                    friend = fi['global_key']
                    # if friend not in each_user_friends:
                    each_user_friends.append(friend)
                user_all_friends = ','.join(each_user_friends)
                count_num = len(each_user_friends)
                cur.execute(insert_sql, (global_key, count_num, user_all_friends))
                db.commit()
                all_user_list.append(global_key)
                crawl_user_friends(each_user_friends)
            else:
                wl.wl_error("获取friends-api的json数据状态码错误,状态码为: {0}, url为: {1}".format(f_json['code'], friends_api))
        else:
            wl.wl_error("访问{0}错误, HTTP状态码为: {1}".format(friends_api, fr.status_code))


def crawl_user_followers(global_key):
    """
    获取用户的粉丝列表
    :param global_key 用户的全局唯一标识
    :return:
    """
    followers_api = 'https://coding.net/api/user/followers/{}?page=1&pageSize=999999999'.format(global_key)


def main():
    hot_users = crawl_best_user()
    if not hot_users:
        wl.wl_error('未获取到种子用户信息')
        db.close()
    if len(set(all_user_list) - set(hot_users)) > 0 and len(all_user_list) > 1:  # 判断是否需要断点抓取
        wl.wl_info("从数据库结果开始继续抓取,当前库用户: {}".format(",".join(all_user_list)))
        crawl_user_friends(all_user_list)
    else:
        wl.wl_info('从热门用户开始抓取,当前热门用户: {}'.format(",".join(hot_users)))
        crawl_user_friends(hot_users)
    db.close()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: toddler
# update: 20171029

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

wl = WriteLog(re_joint_dir_by_os("..|Logs|crawl_all_user.log"))

db_path = re_joint_dir_by_os('..|Data|analyzecoding.db')
db = sqlite3.connect(db_path)
cur = db.cursor()

# 改为更新字段，若数据已经存在，但是用户有了新的社交关系，也要重新入库
insert_sql = "REPLACE INTO coding_all_user (global_key, friends_count, friends, followers_count, followers) VALUES (?, ?, ?, ?, ?)"

cur.execute("SELECT global_key FROM coding_all_user")
temp_query_db_users = cur.fetchall()
if len(temp_query_db_users) > 0:
    db_users = [item[0] for item in temp_query_db_users]
    all_user_list = db_users
else:
    all_user_list = ['coding']  # 初始化一个共有用户, 此用户无friends_api与followers_api


def check_need_save(global_key):
    """
    校验此用户数据是否已经入库
    :param global_key: 用户全局唯一标识
    :return: True需要入库, False不需要入库
    """
    try:
        cur.execute("SELECT count(*) FROM coding_all_user WHERE global_key=?", (global_key,))
        check_res = cur.fetchone()[0]
        if check_res == 0:  # 未入库
            return True
        else:
            return False
    except Exception as check_err:
        wl.wl_error("校验此用户{0}是否已经入库发生错误: {1}".format(global_key.encode('utf-8'), check_err))
        return True


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
        if global_key == 'coding':
            continue
        each_user_friends = list()
        next_loop = list()
        try:
            friends_api = 'https://coding.net/api/user/friends/{0}'.format(global_key.encode('utf-8'))
        except Exception, url_api_err:
            wl.wl_error("拼接获取朋友API-URL错误: {}".format(url_api_err))
            continue
        fr = requests.get(friends_api, params=payload)
        if fr.status_code == 200:
            f_json = fr.json()
            if f_json['code'] == 0:
                num_friends = f_json['data']['totalRow']
                user_friends_info = f_json['data']['list']
                for fi in user_friends_info:
                    friend = fi['global_key']
                    if check_need_save(friend):  # 若用户没有入库则加入抓取队列
                        next_loop.append(friend)
                    each_user_friends.append(friend)
                user_friends = ','.join(each_user_friends)
                follower_res = crawl_user_followers(global_key)  # 获取用户的粉丝数据
                if follower_res:
                    num_followers = follower_res[0]
                    user_followers = follower_res[1]
                else:  # 若获取粉丝数据失败则置为空
                    num_followers = u""
                    user_followers = u""
                try:
                    cur.execute(insert_sql,
                                (global_key, num_friends, user_friends, num_followers, user_followers))
                    db.commit()
                    wl.wl_info("当前抓取用户入库成功: {}".format(global_key.encode('utf-8')))
                except Exception as save_err:
                    wl.wl_error("当前抓取用户入库失败: {0}, 报错信息: {1}".format(global_key.encode('utf-8'), save_err))
                if len(next_loop) > 0:  # 判断是否要进行下一次迭代
                    crawl_user_friends(next_loop)
                else:
                    continue
            else:
                wl.wl_error("获取friends-api的json数据状态码错误,状态码为: {0}, url为: {1}".format(f_json['code'], friends_api))
        else:
            wl.wl_error("访问{0}错误, HTTP状态码为: {1}".format(friends_api, fr.status_code))


def crawl_user_followers(__global_key):
    """
    获取用户的粉丝列表
    :param __global_key 用户全局唯一标识
    :return: list
    """
    each_user_followers = list()
    __payload = {
        'page': '1',
        'pageSize': '999999999'
    }
    try:
        followers_api = 'https://coding.net/api/user/followers/{0}'.format(__global_key.encode('utf-8'))
    except Exception, url_api_err:
        wl.wl_error("拼接获取粉丝API-URL错误: {}".format(url_api_err))
        return False
    __fr = requests.get(followers_api, params=__payload)
    if __fr.status_code == 200:
        __f_json = __fr.json()
        if __f_json['code'] == 0:
            num_followers = __f_json['data']['totalRow']
            user_friends_info = __f_json['data']['list']
            for fi in user_friends_info:
                follower = fi['global_key']
                each_user_followers.append(follower)
            user_followers = ','.join(each_user_followers)
            return num_followers, user_followers
        else:
            wl.wl_error("获取followers-api的json数据状态码错误,状态码为: {0}, url为: {1}".format(__f_json['code'], followers_api))
    else:
        wl.wl_error("访问{0}错误, HTTP状态码为: {1}".format(followers_api, __fr.status_code))


def main():
    hot_users = crawl_best_user()
    if not hot_users:
        wl.wl_error('未获取到种子用户信息')
        db.close()
    if len(set(all_user_list) - set(hot_users)) > 0 and len(all_user_list) > 1:  # 判断是否需要断点抓取
        wl.wl_info("从数据库结果开始继续抓取,当前库用户个数: {}".format(str(len(all_user_list))))
        crawl_user_friends(all_user_list)
    else:
        wl.wl_info('从热门用户开始抓取,当前热门用户: {}'.format(",".join(hot_users)))
        crawl_user_friends(hot_users)
    db.close()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: toddler

import requests
import sqlite3
import sys

sys.path.append("..")
from Lib.my_lib import WriteLog, re_joint_dir_by_os, load_user_agents, div_list

wl = WriteLog(re_joint_dir_by_os("..|Logs|crawl_user_info.log"))

db_path = re_joint_dir_by_os('..|Data|analyzecoding.db')
db = sqlite3.connect(db_path)
cur = db.cursor()


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


def get_all_user_global_key():
    """
    获取库中存储的用户的global_key
    :return: list
    """
    query_db_users_sql = "SELECT global_key FROM coding_all_user"
    cur.execute(query_db_users_sql)
    temp_query_db_users = cur.fetchall()
    db_users = [item[0] for item in temp_query_db_users]
    if len(db_users) > 0:
        wl.wl_info("数据库中共计有{}个用户待抓取用户信息".format(len(db_users)))
        return db_users
    else:
        wl.wl_info("数据库中没有待完善信息的用户账号")
        return False


def get_each_user_info(users_gk):
    """
    获取每一个用户的个人信息
    :param users_gk: 待抓取用户的global_key列表
    :return:
    """
    for global_key in users_gk:
        #if not check_need_save(global_key):  # 如果已经在库中则跳过
        #    continue
        try:
            user_info_api = "https://coding.net/api/user/key/{}".format(global_key.encode('utf-8'))
            wl.wl_info("当前爬取用户URL为: {}".format(user_info_api.encode('utf-8')))
        except Exception, url_api_err:
            wl.wl_error("拼接获取用户信息API-URL错误: {}".format(url_api_err))
            continue
        try:
            r = requests.get(user_info_api)
        except requests.RequestException as r_err:
            wl.wl_error('请求访问{0}失败: {1}'.format(user_info_api, r_err))
            continue
        if r.status_code == 200:
            res_json = r.json()
            if res_json["code"] == 0:
                u_data = res_json['data']

                user_name = u_data['name']
                name_pinyin = u_data['name_pinyin']
                sex_value = u_data['sex']
                if sex_value == 0:
                    sex = u'男'
                elif sex_value == 1:
                    sex = u'女'
                else:
                    sex = u'其他'
                slogan = u_data['slogan']
                company = u_data['company']
                try:
                    job = u_data['job_str']
                except Exception as job_str_get_err:
                    wl.wl_error("此用户的job_str信息获取失败: {}".format(job_str_get_err))
                    job = u""
                tags = u_data['tags_str']
                try:
                    temp_skills = u_data['skills']
                except Exception as skill_get_err:
                    wl.wl_error("此用户的skills信息获取失败: {}".format(skill_get_err))
                    temp_skills = u""
                if len(temp_skills) > 0:
                    skill_list = list()
                    for skill in temp_skills:
                        skill_level = skill['level']
                        skill_name = skill['skillName']
                        each_skill = ":".join([skill_name, str(skill_level)])
                        skill_list.append(each_skill)
                    skills = ','.join(skill_list)
                else:
                    skills = u""
                website = u_data['website']
                introduction = u_data['introduction']
                avatar = u_data['avatar']
                try:
                    school = u_data['school']
                except Exception as school_get_err:
                    wl.wl_error("此用户的school信息获取失败: {}".format(school_get_err))
                    school = u''
                follows_count = u_data['follows_count']
                fans_count = u_data['fans_count']
                tweets_count = u_data['tweets_count']
                vip = u_data['vip']
                created_at = u_data['created_at']
                last_logined_at = u_data['last_logined_at']
                last_activity_at = u_data['last_activity_at']
                insert_data = (
                global_key.decode('utf-8'), user_name, name_pinyin, sex, slogan, company, job, tags, skills, website,
                introduction, avatar, school, follows_count, fans_count, tweets_count, vip, created_at, last_logined_at,
                last_activity_at)
                yield insert_data
            else:
                wl.wl_error("获取user_key-api的json数据状态码错误,状态码为: {0}, url为: {1}".format(res_json['code'], user_info_api))
        else:
            wl.wl_error("访问{0}错误, HTTP状态码为: {1}".format(user_info_api, r.status_code))


def main():
    users = get_all_user_global_key()
    if users:  # 如果从库中发现用户则开始抓取
        insert_sql = "REPLACE INTO coding_user_info " \
                     "(global_key, user_name, name_pinyin, sex, slogan, company, job, tags, skills, website, introduction, avatar, school, follows_count, fans_count, tweets_count, vip, created_at, last_logined_at, last_activity_at)" \
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        div_all_user = div_list(users, (len(users) / 1000))  # 把所有用户以1000个为一组切分处理
        for each_group in div_all_user:
            group_user_info = get_each_user_info(each_group)
            for user in group_user_info:
                try:
                    cur.execute(insert_sql, user)
                except Exception as insert_err:
                    wl.wl_error("数据入库coding_user_info失败, 报错信息: {}".format(insert_err))
                    wl.wl_error("错误数据: {}".format(",".join(user)))
            db.commit()  # 1000个用户提交一次
    db.close()


if __name__ == '__main__':
    main()

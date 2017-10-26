#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: toddler

import requests
import sys


def crawl_best_user():
    """
    获取排行第一的热门用户
    :return:
    """
    base_url = "https://coding.net"
    url_best_user = "https://coding.net/api/tweet/best_user"
    bu_resp = requests.get(url_best_user)
    if bu_resp.status_code != 200:
        print '无法访问热门用户URL'
        sys.exit()
    else:
        try:
            temp_json_data = bu_resp.json()
            if temp_json_data['code'] == 0:
                users_data = temp_json_data['data'][0]
                global_key = users_data['global_key']
                return global_key
            else:
                print "获取热门用户信息异常, json状态码不为0"
                return False
        except requests.RequestException as err:
            raise err


def crawl_user_homepage(global_key):
    """
    获取用户的个人主页信息
    :param global_key 用户的全局唯一标识
    :param user_path 个人主页地址
    :return:
    """
    user_info_api = "https://coding.net/api/user/key/{}".format(global_key)
    r = requests.get(user_info_api)
    if r.status_code == 200:
        res_json = r.json()
        if res_json["code"] == 0:
            u_data = res_json['data']
            user_name = u_data['name']
            user_name_pinyin = u_data['name_pinyin']
            user_updated_at = u_data['updated_at']
            user_path = u_data['path']
            user_is_member = u_data['is_member']
            user_vip = u_data['vip']
            user_vip_expired_at = u_data['vip_expired_at']
            user_follows_count = u_data['follows_count']
            user_fans_count = u_data['fans_count']
            user_tweets_count = u_data['tweets_count']
            user_tags_str = u_data['tags_str']
            user_job_str = u_data['job_str']
            user_sex = u_data['sex']
            user_location = u_data['location']
            user_company = u_data['company']
            user_slogan = u_data['slogan']
            user_website = u_data['website']
            user_introduction = u_data['introduction']
            user_avatar = u_data['avatar']
            user_created_at = u_data['created_at']
            user_last_logined_at = u_data['last_logined_at']
            user_last_activity_at = u_data['last_activity_at']





def main():
    gk, up = crawl_best_user()
    crawl_user_homepage(gk, up)


if __name__ == '__main__':
    main()
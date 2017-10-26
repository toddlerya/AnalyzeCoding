#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: toddler

import requests

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

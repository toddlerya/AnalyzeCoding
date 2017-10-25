#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: toddler

import requests
import sys


def get_best_user():
    """
    获取热门用户信息
    :return:
    """
    url_best_user = "https://coding.net/api/tweet/best_user"
    bu_resp = requests.get(url_best_user)
    if bu_resp.status_code != 200:
        print '获取热门用户失败'
        sys.exit()
    else:
        try:
            temp_json_data = bu_resp.json()
            if temp_json_data[code] == 0:
                pass
        except requests.RequestException as err:
            raise err





def main():
    get_best_user()


if __name__ == '__main__':
    main()
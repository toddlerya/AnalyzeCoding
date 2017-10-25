#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: toddler
# date: 20171025


from lxml import etree
import requests


proxy_type = ['/', '/gngn/', '/gnpt/', '/gwgn/', '/gwpt/']
data5u_url = "http://www.data5u.com/free{}index.shtml"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3387.400 QQBrowser/9.6.11984.400'}


def test_proxy(proxy, test_url):
    """
    测试IP代理是否可用
    测试IP代理是否可用
    :param proxy: 代理配置 ip:port
    :return:
    """
    print 'testing {}'.format(proxy)
    proxies = {"http": proxy}
    try:
        resp = requests.get(url=test_url, proxies=proxies)
        if resp.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def get_free_proxy(goal_url):
    """
    爬取免费IP代理，返回IP代理池
    :param goal_url 目标访问的网址 goal_url
    :return:
    """
    free_proxy_list = list()
    for item in proxy_type:
        url = data5u_url.format(item)
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print "无法访问 {}".format(url)
            return False
        else:
            html = r.text.encode('utf-8')
            if u'代理'.encode('utf-8') in html:
                selector = etree.HTML(html)
                ip_port_ul = selector.xpath('//ul[@class="l2"]')
                for li in ip_port_ul:
                    li_texts = li.xpath('.//li/text()')
                    ip_port = ':'.join(li_texts[0:2])
                    try:
                        quality = int(li_texts[2].split('.')[0])
                    except:
                        continue
                    if quality < 5:  # 延迟小于2秒的进行测试
                        if test_proxy(ip_port, goal_url):  # 测试通过放入代理池
                            free_proxy_list.append(ip_port)
            else:
                return False
    free_proxy_pool = list(set(free_proxy_list))
    return len(free_proxy_pool), free_proxy_pool


if __name__ == '__main__':
    print get_free_proxy("https://coding.net")

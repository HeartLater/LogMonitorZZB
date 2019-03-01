#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Yampery

"""
    对audit（用户操作）日志的处理
"""

from __future__ import print_function
from __future__ import absolute_import
import re
import dboption

# 匹配以固定时间格式开始的字符串
PATTERN = re.compile(r'(\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2}:\d{1,2}).*')


def filter_line(line):
    """读取一行并判断是否是有效日志
       判断依据，是否以指定格式日期开始
    """
    ret = ''
    if PATTERN.match(line):
        filter_line.cache.append(line)
    if filter_line.cache:
        ret = "".join(filter_line.cache)
        filter_line.cache = []
    return ret


filter_line.cache = []


def gen_read_callback(find_callback):
    """tail检测到新行的回调函数"""
    def _callback(readed):
        content = filter_line(readed)
        if len(content.strip()) > 0:
            find_callback(content)
    return _callback


def handler(s):
    """处理行
       2018-11-06T11:39:39.308+0800, User(admin), RemoteIp(10.0.117.109), Operation(Configuration change)
    """
    po = {
        'User': '',
        'RemoteIp': '',
        'Operation': ''
    }
    l = s.split(',')
    # User(admin) -> k(v)
    lk = []  # 存储key
    lv = []  # 存储value
    po['datetime'] = l[0][0:19].replace('T', ' ')
    for i in range(1, len(l)):
        lk = re.findall('(\w+)\(', l[i])
        lv = re.findall('\((.*)\)', l[i])
        if lk and lv:
            po[lk[0]] = lv[0]
    # 调用oracle入库操作
    if po['User'] and 'null' != po['User'] and po['RemoteIp'] and 'null' != po['RemoteIp'] and po['Operation'] and 'null' != po['Operation']:
        dboption.insert(po, handler.orcl)

# 日志文件变动的回调函数，在程序入口引用，如果有其他需求可以更改或添加
callback = gen_read_callback(handler)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author Yampery

from __future__ import print_function
from __future__ import absolute_import
from tail import tails
from audit import callback
from audit import handler
import sys
import json


def main():
    """日志监控程序入口
       在这里调用tails并设置配置参数
    """
    config_file = ''
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        config_file = 'conf/config.json'

    with open(config_file, 'r') as jsonfile:
        config = json.load(jsonfile)

    # 指定配置
    handler.orcl = config['orcl']
    # 调用日志监控，如果多个日志文件，可以启相应个线程执行
    # Tail对象需要继承Thread，本程序并未实现
    tails(config['log_file'], callback)


if __name__ == "__main__":
    main()

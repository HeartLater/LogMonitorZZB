#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Yampery

from __future__ import print_function
from __future__ import absolute_import
import time
from datetime import date
from datetime import datetime


class Tail(object):
    """文件监听，类似于Linux的tail方法
       默认当前初始均从文件末尾开始
       可以通过调用时指定对象构造参数'curr_position'指定偏移量
    """
    MAX_SLEEP_COUNT = 2

    def __init__(self, tailed_file, start=0):
        self.tailed_file = tailed_file
        self.curr_position = start
        self.read_callback = None
        self.sleep_count = 0

    def follow(self, s=30):
        """实时监听文件"""
        with open(self.tailed_file, 'rb') as file_:
            # 程序启动时直接定位到文件末尾
            if (0 == self.curr_position):
                file_.seek(0, 2)
            # 在程序运行期间文件指针已经偏移
            else:
                file_.seek(self.curr_position)
            while True:
                if self.sleep_count == Tail.MAX_SLEEP_COUNT:
                    return self.curr_position

                readed = file_.readline()
                curr_position = file_.tell()
                if (curr_position - self.curr_position < 0):
                    print('curr_position:[%s], self.curr_position:[%s]' % (
                        curr_position, self.curr_position))
                    time.sleep(s)
                    self.sleep_count += 1
                else:
                    self.sleep_count = 0
                    self.curr_position = curr_position
                    if self.read_callback:
                        self.read_callback(readed)

    def register_read_callback(self, callback):
        self.read_callback = callback


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def tails(file_pattern, callback):
    """tail文件"""
    # 从文件末尾开始，防止程序重启导致数据读取重复
    # @TODO 最好用一个文件记录上次程序关闭之前读到位置(但是如果是异常结束，应该怎么确定位置)
    # 这样就可以使用seek(pos)从开始定位到上次读的行数，这里暂时不做处理
    # with open('file.pos', 'w+') as pos_:

    start_read = 0
    today = date.today()
    while True:
        file_name = today.strftime(file_pattern)
        print("%s Info: [start tail file: '%s']" % (now_str(), file_name))
        if today < date.today():
            start_read = 0

        today = date.today()
        try:
            t = Tail(file_name, start_read)
            t.register_read_callback(callback)
            start_read = t.follow()
        except IOError, e:
            print("%s, Error: [cannot tail log file: %s], Reason: [%s]" %
                  (datetime.now(), file_name, str(e)))
            time.sleep(60)

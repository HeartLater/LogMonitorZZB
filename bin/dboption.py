#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Yampery

import cx_Oracle
from datetime import datetime


class OracleOpt(object):
    """oracle数据库映射"""

    def __init__(self, conf):
        self.conf = conf


def insert(po, orcl):
    """Parameter:
            po: 将字符串切割后的对象
            orcl: oracle的配置参数
       Description:
            将日志文件一行内容中有用的字段插入数据库
    """
    conn = cx_Oracle.connect(
        orcl['username'], orcl['password'], '%s/%s' % (orcl['host'], orcl['servername']))
    cursor = conn.cursor()
    id = 1
    cursor.execute('select max(LOGID) from %s.WCMLOG' % orcl['database'])
    row = cursor.fetchone()
    if row and row[0]:
        id = row[0] + 1
    sql = "insert into %s.WCMLOG (LOGID,LOGUSER,LOGTYPE,LOGOBJTYPE,LOGOPTIME,LOGUSERIP,LOGDESC) values (%s,'%s',%s,%s,to_date('%s','YYYY-MM-DD HH24:MI:SS'),'%s','%s')" % (
        orcl['database'], id, po['User'], 3, 0, po['datetime'], po['RemoteIp'], po['Operation'])
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print datetime.now(), "Error: [%s], Reason: [%s]" % (sql, str(e))
    else:
        pass
    finally:
        cursor.close()
        conn.close()


""" 
if __name__ == '__main__':
    with open('conf/config.json', 'r') as jsonfile:
        jsonval = json.load(jsonfile)
    # 测试连接
    query(jsonval['orcl'])
"""

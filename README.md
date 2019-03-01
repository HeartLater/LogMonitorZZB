# logmonitor日志提取#

> 实时监控后台日志文件并对日志进行切割，将需要的字段入库

- run.py 程序入口
- tail.py 日志实时监控
- audit 用户操作日志处理
- dboption 数据库操作

-------------------------------------

## 配置文件conf/config.json

```json
{
    "log_file": "/var/log/ambari-server/ambari-audit.log",
    "orcl": {
        "host": "127.0.0.1",
        "servername": "orcl.xdata",
        "database": "SCOTT",
        "username": "admin",
        "password": "admin123"
    }
}
```

- log_file: 要监控的日志文件
- orcl: oracle数据库配置

-------------------------------------

## 部署

### 环境

- python2.6以上
- oracle11g

### oracle客户端环境

```sh
# 进入libs文件夹下，直接安装
rpm -ivh oracle-instantclient-11.2.0.2.0-11.2.x86_64.rpm
```
### cx_Oracle包安装

```sh
# 进入libs文件夹
# 解压
tar -xzvf cx_Oracle-7.0.0.tar.gz
# 进入cx_Oracle-7.0.0目录安装
python setup.py install
```

---------------------------------------

## 运行

> 配置文件必须符合conf/config.json格式，如果不指定配置文件位置，默认使用conf/config.json

*使用脚本运行*
```sh
# 按上述要求做好配置文件之后，执行脚本
# 启动
sh monitor.sh start
# 指定配置文件运行
sh monitor.sh start conf/config.json
# 停止
sh monitor.sh stop
```

*使用python执行*

```sh
# 在logmonigor目录下执行
# 调试运行
python bin/run.py config_path
# 线上运行，bin目录下执行，console.log仅有异常日志
nohup python bin/run.py config_path > logs/console.log &
```
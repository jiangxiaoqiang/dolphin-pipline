#!/usr/bin/env bash

# 当使用未初始化的变量时，程序自动退出
set -u

# 当任何一行命令执行失败时，自动退出脚本
set -e

set -x

nohup python3 manage.py runserver 0.0.0.0:9000 >> /dev/null &

sleep 5s

curl http://127.0.0.1:9000/spider/api/v1/consumer


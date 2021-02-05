# -*-coding:utf-8 -*-
# !/usr/bin/python
__author__ = 'dongjie'
__data__ = '2015-05-20'

''' 配置系统相关的参数,提供全局的相关配置 '''
import os
import sys
root_dir = '/'.join(os.path.realpath(__file__).split('/')[:-1])
sys.path.append(root_dir)
# log等级,1:notset 2:debug 3:info 4:warning 5:error 6:critical
logLevel = 2
# 日志文件路径
logFile = os.path.join(root_dir, 'logs')

# 数据库配置，支持MYSQL、MSSQL、ORACLE
DATABASE = {
    "ENGINE": "MSSQL",
    "HOST": "",
    "PORT": 3433,
    "USER": "",
    "PWD": "",
    "DATABASE": ""
}
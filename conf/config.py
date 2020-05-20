#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "张开"
# Date: 2019/11/25

import os
import datetime

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_PATH, 'data')


# 测试脚本文件名
file_name = '接口测试示例-2.xlsx'
TEST_CASE_FILE_NAME = os.path.join(DATA_PATH, file_name)


# ---------------- 日志相关 --------------------
# 日志级别
LOG_LEVEL = 'debug'
LOG_STREAM_LEVEL = 'debug'  # 屏幕输出流
LOG_FILE_LEVEL = 'info'   # 文件输出流

# 日志文件命名

LOG_FILE_NAME = os.path.join(BASE_PATH, 'logs', datetime.datetime.now().strftime('%Y-%m-%d') + '.log')


# ----------------- allure 相关 ----------------
# 生成allure报告命令
result_path = os.path.join(BASE_PATH, 'report', 'result')
allure_html_path = os.path.join(BASE_PATH, 'report', 'allure_html')
ALLURE_COMMAND = 'allure generate {} -o {} --clean'.format(result_path, allure_html_path)

# allure报告路径
ALLURE_REPORT_PATH = os.path.join(BASE_PATH, 'report')

# ------------ 邮件相关配置 --------------
MAIL_HOST = "smtp.qq.com"  # 设置服务器
MAIL_USERNAME = "你的qq邮箱"  # 用户名
MAIL_PASSPHRASE = "你的QQ授权码"  # 口令
MAIL_SENDER = '12061xxx@qq.com'   # 发件人
MAIL_RECEIVED = ['1206xxxxx@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
# 邮件主题
MAIL_SUBJECT = '{} 执行{}的测试报告'.format(datetime.datetime.now().strftime('%Y-%m-%d'), file_name)
# 邮件正文
MAIL_CONTENT = '请查阅 - {}\n注意，在解压后使用pycharm打开'.format(MAIL_SUBJECT)

if __name__ == '__main__':
    print(ALLURE_COMMAND)
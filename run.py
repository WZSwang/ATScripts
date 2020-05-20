#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "张开"
# Date: 2019/11/25

import os
import sys
import shutil
import pytest
#
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#
# os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from conf.settings import BASE_DIR
from utils.AllureHandler import AllureOperate

if __name__ == '__main__':
    # 删除之前的json文件

    # print(os.getcwd())
    dir_path = os.path.join(BASE_DIR, 'report', 'json_result')
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
    # 更改工作目录
    # os.chdir(BASE_DIR)
    # 执行用例
    pytest.main()
    # 生成allure报告
    allure_obj = AllureOperate()
    allure_obj.get_allure_report()
    # 压缩文件
    # allure_obj.check_zip()
    # 发邮件
    # allure_obj.send_mail()

#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "张开"
# Date: 2019/11/25

import json
import re
import requests
from jsonpath_rw import parse
from utils.LoggerHandler import logger
from utils.ExcelHandler import ExcelOperate
log = logger()

class RequestHandler(object):
    """ 请求相关 """


    def __init__(self, current_case, all_case_data):
        self.current_case = current_case
        self.all_case_data = all_case_data
        # 下面的try是判断返回值是json类型还是文本类型
        # try:
        #     self.case_except = json.loads(self.current_case.get('case_expect'))
        # except:
        #     self.case_except = self.current_case.get('case_expect')
    @property
    def get_response(self):
        # 查看用例是否有前置依赖
        # self._check_precondition()

        # 从case中获取参数发送请求
        response = self.send_request()
        return response

    def send_request(self):
        """ 发送请求 """
        # try:
        response = requests.request(
            method=self.current_case.get('method'),
            url=self.current_case.get('url'),
            params=self._check_params(),
            data=self._check_data(),
            cookies=self._check_cookies(),
            json=self._check_json(),
            headers=self._check_headers(),
        )
        # print('---------请求结果--------->', response.json(), '\n', self.current_case)
        self._write_data_msg(response=response)

    def _write_data_msg(self, response):
        """
        将请求的响应结果都写入到当前case的字典中
        response: 请求的结果对象
        """
        for index, line in enumerate(self.all_case_data, 0):
            if line['case_num'] == self.current_case['case_num']:
                # 写 headers
                self.all_case_data[index]['template_response_headers'] = response.headers
                # 如果有cookies，写入
                if response.cookies.get_dict():
                    self.all_case_data[index]['template_response_cookies'] = response.cookies.get_dict()
                else:
                    self.all_case_data[index]['template_response_cookies'] = {}
                # 写响应结果 json
                if response.headers['Content-Type'].lower() == "application/json;charset=utf-8":
                    self.all_case_data[index]['template_response_json'] = response.json()

                # 将 请求参数也重新写一份，后续可能会用到
                    self.all_case_data[index]['template_response_data'] = self.current_case['data']
                    self.all_case_data[index]['template_response_params'] = self.current_case['params']


            # 这部分可以写的很复杂的，因为要根据具体的业务来设计不同的用例，复杂度也不相同，这里简单来实现
            # 根据请求头判断是什么类型的返回
        #     content_type = response.headers.get('Content-Type')
        #     content_type = content_type.split(';')[0].split('/')[-1] if ';' in content_type else content_type.split('/')[-1]
        #     if hasattr(self, '_check_{}_response'.format(content_type)):
        #         response = getattr(self, '_check_{}_response'.format(content_type))(response)
        #     else:
        #         raise '不支持的返回类型'
        # except Exception as e:
        #     print(e)
        #     log.error('{} {}'.format(self.current_case.get('case_url'), e))
        #     return {"response": e}, self.case_except
        # return response

    # def _check_json_response(self, response):
    #     """ 本次请求返回的类型是json类型 """
    #     # 这里也可以很复杂，只是简单来写
    #     response = response.json()
    #     for k in self.case_except:
    #         if self.case_except[k] != response.get(k):
    #             return {k: self.case_except[k]}, {k: response.get(k)}
    #     return {k: self.case_except[k]}, {k: response.get(k)}
    #
    # def _check_html_response(self, response):
    #     """ 本次请求返回的类型是 html 类型 """
    #     # 这里也可以很复杂，只是简单来写,判断html类型的数据title对的上号就行
    #     return response.title, self.case_except


    def _check_params(self):
        """ 检校验 params 参数，是否有依赖要处理"""
        params = self.current_case.get("params", None)
        if params:
            return self._re_operation(parameter=params)
        else:
            return {}



    def _check_data(self):
        """ 校验 data 参数，是否有依赖要处理"""
        data = self.current_case['data']
        if data:
            return self._re_operation(parameter=data)
        else:
            return {}





    def _check_cookies(self):
        """ 校验 是否需要携带 cookies """
        cookies = self.current_case['cookies']
        if cookies:
            # print(11111111, cookies)
            for line in self.all_case_data:

                if line['case_num'] == cookies:
                    temp_cookies =line['template_response_cookies']
                    if isinstance(temp_cookies, str):
                        return json.loads(temp_cookies)
                    else:
                        return temp_cookies
        else:
            return {}

    def _check_headers(self):
        """ 校验  headers 参数，是否有依赖要处理 """
        headers = self.current_case['headers']
        if headers:
            return self._re_operation(headers)
        else:
            return {}



    def _check_json(self):
        """ 校验  json 参数，是否有依赖要处理 """
        temp_json = self.current_case['json']
        if temp_json:
            return self._re_operation(temp_json)
        else:
            return {}


    def _re_operation(self, parameter):
        """
        使用 re 来处理有依赖的参数
        :param parameter: 各种类型的参数，如 header，data
        :return: 处理后的数据
        """
        if isinstance(parameter, dict):  # 传过来的参数可能是 str 但也要保证没有 dict 类型的，后续的操作基于 str 来
            parameter = json.dumps(parameter)
        # 使用正则来查看是否有依赖
        pattern = re.compile("\\${(.*?)}\\$")  # .*? 将多出依赖分开处理
        match_list = pattern.findall(parameter)
        # print(111111111, match_list, parameter, type(parameter))
        if match_list:  # 有依赖需要处理
            for match in match_list:
                case_num, params, json_path = match.split(">")
                # print(2222222, case_num, params, json_path, parameter, type(parameter))
                # jsonpath-rw在找路径的时候，需要的是dict类型，所以要先反序列化
                for line in self.all_case_data:
                    if line['case_num'] == case_num:
                        temp_data = line["template_response_{}".format(params)]
                        if isinstance(temp_data, str):
                            temp_data = json.loads(temp_data)
                        # print(111111111, temp_data, type(temp_data), parameter)
                        rule_data = parse(json_path).find(temp_data)
                        if rule_data:
                            rule_data = [v.value for v in rule_data][0]
                        parameter = re.sub(pattern, rule_data, parameter, 1)
                        # print(11111111, rule_data, parameter, type(parameter))
            # print(222222, parameter, type(parameter))
            return json.loads(parameter)

        else:
            if isinstance(parameter, str):
                parameter = json.loads(parameter)
            return parameter

if __name__ == '__main__':
    import os
    from conf import config
    # data_list = ExcelOperate(file_path=os.path.join(config.DATA_PATH, '接口测试示例-2.xlsx'), sheet_by=2).get_dict_sheet()
    # for i in data_list:
    #     RequestHandler(current_case=i, all_case_data=data_list).get_response
    # print('原始列表----------', data_list)


"""

处理请求
"""
import re
import json
import requests
from jsonpath_rw import parse
from urllib.parse import urlparse
from conf import settings
from utils.LogHandler import logger


# ---------------  有数cookies依赖的写法-2 ---------------------




class RequestsOperate(object):

    def __init__(self, current_case, all_excel_data_list):
        self.current_case = current_case
        self.all_excel_data_list = all_excel_data_list


    def get_response_msg(self):
        """ 发送请求并且获取结果 """
        return self._send_msg()

    def _send_msg(self):
        """ 发请求 """
        # print(1111111111, self.current_case)
        logger().info('正在向 {} 发送请求，{}'.format(self.current_case['url'], self.current_case))
        response = requests.request(
            method=self.current_case['method'],
            url=self.current_case['url'],
            data=self._check__request_data(),
            params=self._check__request_params(),
            cookies=self._check_request_cookies(),
            headers=self._check_request_headers(),
        )
        # print("------------- {} 请求结果 ----------------".format(self.current_case['case_num']), response.json())
        self._write_cookies(response)

        # print(111111, "预期值", self.current_case['except'], '实际执行结果', response.json())
        return json.loads(self.current_case['except']), response.json()

    def _check_request_headers(self):
        """ 校验请求头 做携带cookis 和 数据依赖的问题 """
        headers = self.current_case.get("headers", None)
        if headers:
            return self._operate_re_msg(headers)

        else:
            return {}

    def _write_cookies(self,response):
        """ 监测响应结果中是否含有cookies，有就保存起来 """
        cookies = response.cookies.get_dict()
        # print(self.current_case)
        for item in self.all_excel_data_list:
            if item['case_num'] == self.current_case['case_num']:
                # print(111111111, item)
                item['temporary_response_cookies'] = response.cookies.get_dict()
                if response.headers['Content-Type'].lower() == 'application/json;charset=utf-8':
                    item['temporary_response_json'] = response.json()
                item['temporary_request_headers'] = self.current_case['headers']
                item['temporary_request_data'] = self.current_case['data']
                item['temporary_request_json'] = self.current_case['json']
                item['temporary_request_params'] = self.current_case['params']
                item['temporary_response_headers'] = response.headers


        # print(self.all_excel_data_list)

    def _check__request_data(self):
        """ 处理 请求的 data 参数，检查是否有依赖 """
        data = self.current_case['data']
        if data:
            # print(data, type(data))
            return json.loads(data)
        else:
            return {}

    def _check__request_params(self):
        """ 处理 请求的 params 参数，检查是否有依赖 """
        params = self.current_case['params']
        if params:
            return json.loads(params)
        else:
            return {}

    def _check_request_cookies(self):
        """ 处理请求中的 cookies """
        cookies_case_num = self.current_case.get("cookies", None)
        # print(1111111111, cookies_case_num)
        if cookies_case_num:  # 当前接口需要cookies
            # print(2222222222, cookies_case_num)
            for item in self.all_excel_data_list:
                if item['case_num'] == cookies_case_num:
                    return item.get('temporary_response_cookies', {})

        else:
            return {}

    def _operate_re_msg(self, parameter):
        """
        正则校验，数据依赖的字段
        :param parameter: 各种参数，如： data,headers, params
        :return:
        """
        # print(22222222,parameter)
        # 使用 re 提取依赖字段  {"testfan-token": "${neeo_001>response_json>data}$"}
        if isinstance(parameter, dict):
            parameter = json.dumps(parameter)
        pattern = re.compile('\${(.*?)}\$')
        rule_list = pattern.findall(parameter)
        # print(333333333, parameter)
        if rule_list:   # 该参数有数据依赖要处理
            for rule in rule_list:
                case_num, params, json_path = rule.split(">")
                # print(333333333, case_num, params, json_path)  # neeo_001 response_json data.info.phone
                for line in self.all_excel_data_list:
                    if line['case_num'] == case_num:
                        # print(11111111111, self.current_case, '\n', params, '\n', line)
                        temp_data = line["temporary_{}".format(params)]
                        # print(temp_data, type(temp_data))
                        if isinstance(temp_data, str):
                            temp_data = json.loads(temp_data)
                        match_list = parse(json_path).find(temp_data)
                        # print(333333333, match_list)
                        if match_list:
                          match_data = [v.value for v in match_list][0]
                        # print(match_data)
                        # 将提取出来的值替换到原来规则 24fcbcc6dc004f3eb9ef13f59160ca7c  --> {"testfan-token": "${neeo_001>response_json>data}$"}
                        parameter = re.sub(pattern=pattern, repl=match_data, string=parameter, count=1)
            return json.loads(parameter)

        else:
            if isinstance(parameter, str):
                parameter = json.loads(parameter)
            return parameter




# ---------------  有数cookies依赖的写法-1 ---------------------


# class RequestsOperate(object):
#
#     def __init__(self, current_case):
#         self.current_case = current_case
#
#     def get_response_msg(self):
#         """ 发送请求并且获取结果 """
#         self._send_msg()
#
#     def _send_msg(self):
#         """ 发请求 """
#         response = requests.request(
#             method=self.current_case['method'],
#             url=self.current_case['url'],
#             data=self._check__request_data(),
#             params=self._check__request_params(),
#             cookies=self._check_request_cookies(),
#             # headers=self._check_request_headers(self.current_case['url']),
#         )
#         print("------------- 请求结果 ----------------", response.json(), response.cookies.get_dict(), response.headers, '\n', "------------- 请求结果 ----------------")
#         self._write_cookies(response)
#
#     def _check_request_headers(self, url):
#         """ 校验请求头 做携带cookis 和 数据依赖的问题 """
#
#         """
#             {
#                 'user': '${}$',
#                 'testfan-id': 'f4d323c6-a45e-4105-9b22-812fc6727067'
#             }
#         """
#         # netloc = urlparse(url=url).netloc
#         # # print(1111111, netloc)
#         # temp_data = settings.COOKIES_DICT.get(netloc, None)
#         # print(111111, temp_data)
#         # headers = {
#         #     # "Cookie": {'testfan-id': 'c5844ef7-256e-418f-ac4c-91277a52fe9f'}
#         # }
#         # if temp_data:
#         #     # pass
#         #     headers["cookies"] = json.dumps(temp_data)
#         # # print(111111111, headers)
#         # return headers
#         return {}
#
#
#     def _write_cookies(self,response):
#         """ 监测响应结果中是否含有cookies，有就保存起来 """
#         cookies = response.cookies.get_dict()
#         if cookies:
#             netloc = urlparse(url=response.url).netloc
#             settings.COOKIES_DICT[netloc] = cookies
#             # print(2222222222, settings.COOKIES_DICT)
#         else:
#             pass
#
#     def _check__request_data(self):
#         """ 处理 请求的 data 参数，检查是否有依赖 """
#         data = self.current_case['data']
#         if data:
#             # print(data, type(data))
#             return json.loads(data)
#         else:
#             return {}
#
#     def _check__request_params(self):
#         """ 处理 请求的 params 参数，检查是否有依赖 """
#         params = self.current_case['params']
#         if params:
#             return json.loads(params)
#         else:
#             return {}
#
#     def _check_request_cookies(self):
#         """ 处理请求中的 cookies """
#         if self.current_case['cookies']:
#             # 获取当前的url的域名
#             netloc = urlparse(url=self.current_case['url']).netloc
#             # 根据域名从配置文件中取该域名下的cookies
#             cookies = settings.COOKIES_DICT.get(netloc, None)
#             if cookies:  # 如果有cookies要携带
#                 return cookies
#             else:
#                 return {}
#         else:
#             return {}









# --------------- 没有依赖的写法 -------------------------------

# class RequestsOperate(object):
#
#     def __init__(self, current_case):
#         self.current_case = current_case
#
#     def get_response_msg(self):
#         """ 发送请求并且获取结果 """
#         self._send_msg()
#
#
#     def _send_msg(self):
#         """ 发请求 """
#         response = requests.request(
#             method=self.current_case['method'],
#             url=self.current_case['url'],
#             data=self._check__request_data(),
#             params=self._check__request_params(),
#         )
#         print("------------- 请求结果 ----------------", response.json(), '\n', "------------- 请求结果 ----------------")
#
#     def _check__request_data(self):
#         """ 处理 请求的 data 参数，检查是否有依赖 """
#         data = self.current_case['data']
#         if data:
#             # print(data, type(data))
#             return json.loads(data)
#         else:
#             return {}
#
#     def _check__request_params(self):
#         """ 处理 请求的 params 参数，检查是否有依赖 """
#         params = self.current_case['params']
#         if params:
#             return json.loads(params)
#         else:
#             return {}


if __name__ == '__main__':
    from utils.ExcelHandler import ExcelOperate
    from conf import settings

    excel_data_list = ExcelOperate(settings.FILE_PATH, sheet_by_index=3).get_excel()
    for item in excel_data_list:
        RequestsOperate(current_case=item, all_excel_data_list = excel_data_list).get_response_msg()
        # print(item)

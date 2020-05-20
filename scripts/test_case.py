

import os
import shutil
import pytest
import allure
from deepdiff import DeepDiff
from utils.ExcelHandler import ExcelOperate
from utils.RequestsHandler import RequestsOperate
from utils.LogHandler import logger
from conf import settings

excel_data_list = ExcelOperate(settings.FILE_PATH, 3).get_excel()







class TestCase(object):

    # @classmethod
    # def setup_class(cls):
    #     cls.excel_data_list = ExcelOperate(settings.FILE_PATH, 0).get_excel()

    @pytest.mark.parametrize('item', excel_data_list)
    def test_case(self, item):
        logger().info('正在进行断言.....')
        except_date, result = RequestsOperate(current_case=item, all_excel_data_list=excel_data_list).get_response_msg()
        # print(DeepDiff(except_date, result))
        allure.dynamic.title(item['title'])

        allure.dynamic.description(
            "<b style='color:red'>请求的url:</b>{}<hr />"
            "<b style='color:red'>预期值: </b>{}<hr />"
            "<b style='color:red'>实际执行结果: </b>{}<hr />".format(item['url'], item['except'], result)
        )


        assert not DeepDiff(except_date, result).get('values_changed', None)

        logger().info('完成断言，{}'.format(except_date, result))

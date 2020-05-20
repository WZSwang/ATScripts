"""
处理Excel
"""

import xlrd
from conf import settings
from utils.LogHandler import logger


class ExcelOperate(object):

    def __init__(self, file_path, sheet_by_index=0):
        self.file_path = file_path
        self.sheet_by_index = sheet_by_index
        book = xlrd.open_workbook(self.file_path)
        self.sheet = book.sheet_by_index(self.sheet_by_index)

    def get_excel(self):
        """ 获取Excel数据 """
        # l = []

        title = self.sheet.row_values(0)
        # print(title)
        # for row in range(1, self.sheet.nrows):
        #     l.append(dict(zip(title, self.sheet.row_values(row))))
        # return l
        # print(1111, self.sheet.nrows)
        l = [dict(zip(title, self.sheet.row_values(row))) for row in range(1, self.sheet.nrows)]
        logger().info('读取Excel 成功，数据已返回')
        return l

if __name__ == '__main__':
    excel_data_list = ExcelOperate(settings.FILE_PATH, 2).get_excel()
    print(excel_data_list)













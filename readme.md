

# 接口自动化
本质：通过requests和Excel(数据库)对用例进行批量的自动化回归测试。

# 关于Excel
操作Excel：https://www.cnblogs.com/Neeo/articles/11650149.html


```python
import xlrd
from conf import settings

book = xlrd.open_workbook(settings.FILE_PATH)
sheet = book.sheet_by_index(0)
# book.sheet_by_name('通用接口')
# print(sheet.nrows, sheet.ncols)  # 获取所有行和列数

# 获取指定行

# print(sheet.row_values(0))
# print(sheet.row_values(1))

# 获取指定列
# print(sheet.col_values(0))


l = []
title = sheet.row_values(0)
print(title)
for row in range(1, sheet.nrows):
    l.append(dict(zip(title, sheet.row_values(row))))

print(l)

```


# 如何处理数据依赖

在Excel中编写测试用例的时候：
1. 被依赖的接口用例写在上面
2. 对于依赖的字段设置规则：
    - {"user":"admin", "token":"xxxxadsasdads"}
    - {"token":"${case_001>request_data>token}$"}

# 单元测试框架
pytest


# 关于cookies处理
## 第一种
借鉴postman的cookies管理器，即每个请求都监测响应结果是否有cookies返回，如果有，就保存，以域名的形式保存该cookies

如果有同域名的请求，就自动在headers中携带该cookies

## 第二种
我们在请求中，判断响应结果中是否返回了cookis，如果返回了，就保存到当前的用例对象中，该对象就是一个大的字典。将cookies和值保存为一个key value
谁要用，就来拿该参数


# 关于urllib
参考：https://www.cnblogs.com/Neeo/articles/11520952.html



# 如何删除一个非空目录
用shuitil
```python
import shutil
'''
shutil模块对文件和文件集合提供了许多高级操作。特别是，提供了支持文件复制和删除的功能
'''

# shutil.copy(src, dst)   # 拷贝文件
# shutil.move(src, dst)  # 移动目录或者文件

# shutil.rmtree(path)   # 递归删除目录，无法直接删除文件
# shutil.make_archive(base_name, format('zip'))   # 将目录或者文件以指定格式压缩
# shutil.unpack_archive(filename, extract_dir)  # 解压缩

# see also: https://docs.python.org/3/library/shutil.html

```

# 关于生成测试报告的命令
参考：https://docs.python.org/zh-cn/3/library/subprocess.html


# 关于打包

参考：https://www.cnblogs.com/Neeo/articles/11934072.html

# 日志

参考：https://www.cnblogs.com/Neeo/articles/10951734.html#%E7%A4%BA%E4%BE%8B










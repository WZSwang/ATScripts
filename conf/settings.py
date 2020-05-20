
import os
import datetime
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------- 关于Ecel配置-------------

FILE_NAME = "接口测试示例-2.xlsx"
FILE_PATH = os.path.join(BASE_DIR, 'data', FILE_NAME)

# --------------------- template cookies dict ---------------
COOKIES_DICT = {}



# -------------------- allure 报告相关 ------------



ALLURE_COMMAND = 'allure generate {from_json_path} -o {save_to_path} --clean'.format(
    from_json_path=os.path.join(BASE_DIR, 'report', 'json_result'),
    save_to_path=os.path.join(BASE_DIR, 'report', "allure_result")
)

# ------------------------ 邮件相关 -------------

MAIL_HOST = "smtp.qq.com"  # 设置服务器   # 勿动
MAIL_USER = "你的QQ邮箱@qq.com"  # 用户名
MAIL_TOKEN = "你的授权码"  # 授权码
# 设置收件人和发件人
SENDER = 'xxxx@qq.com'
RECEIVERS = ['xxxxx@qq.com', 'xxxxxx@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# 邮件主题
THEME = '请查阅--s28的第一个测试报告'
# 正文内容
SEND_CONTENT = 'hi man，你收到附件了吗？'

# 附件的file name

SEND_FILE_NAME = 'allure_report.zip'

# ---------------- 日志相关 --------------------
# 日志级别
LOG_LEVEL = 'debug'
LOG_STREAM_LEVEL = 'debug'  # 屏幕输出流
LOG_FILE_LEVEL = 'info'   # 文件输出流

# 日志文件命名

LOG_FILE_NAME = os.path.join(BASE_DIR, 'logs', datetime.datetime.now().strftime('%Y-%m-%d') + '.log')

if __name__ == '__main__':
    print(LOG_FILE_NAME)




















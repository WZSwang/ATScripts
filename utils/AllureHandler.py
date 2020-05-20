"""

allure报告相关
"""


import os
import subprocess
import zipfile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from utils.LogHandler import logger




from conf import settings


class AllureOperate(object):


    def get_allure_report(self):
        """ 生成报告 """

        # os.system(ALLURE_COMMAND)
        # subprocess.Popen(ALLURE_COMMAND, shell=True)
        logger().info('正在生成测试报告.....')
        subprocess.call(settings.ALLURE_COMMAND, shell=True)
        logger().info('生成测试报告成功.....')
        '''
            ["allure", "generate", ]
        '''



    def check_zip(self):
        """ 打包 """
        try:
            logger().info('正在打包测试报告.....')
            # BASE_DIR:当前脚本的父级目录
            BASE_DIR = os.path.join(settings.BASE_DIR, 'report')
            start_zip_dir = os.path.join(BASE_DIR, 'allure_result')  # 要压缩文件夹的根路径
            zip_file_name = 'allure_report.zip'  # 为压缩后的文件起个名字

            zip_file_path = os.path.join(BASE_DIR, zip_file_name)
            f = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
            for dir_path, dir_name, file_names in os.walk(start_zip_dir):
                # 要是不replace，就从根目录开始复制
                file_path = dir_path.replace(start_zip_dir, '')
                # 实现当前文件夹以及包含的所有文件
                file_path = file_path and file_path + os.sep or ''
                for file_name in file_names:
                    f.write(os.path.join(dir_path, file_name), file_path + file_name)
            f.close()
            logger().info('打包测试报告完成.....')
        except Exception as e:
            logger().error('打包测试报告失败: {}'.format(e))


    def send_mail(self):

        # 第三方 SMTP 服务
        mail_host = settings.MAIL_HOST  # 设置服务器   # 勿动
        mail_user = settings.MAIL_USER  # 用户名
        mail_pass = settings.MAIL_TOKEN  # 口令
        # 设置收件人和发件人
        sender = settings.SENDER
        receivers = settings.RECEIVERS

        # 创建一个带附件的实例对象
        message = MIMEMultipart()

        # 邮件主题、收件人、发件人
        subject = settings.THEME  # 邮件主题
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = Header("{}".format(sender), 'utf-8')  # 发件人
        message['To'] = Header("{}".format(';'.join(receivers)), 'utf-8')  # 收件人
        # 邮件正文内容
        send_content = settings.SEND_CONTENT
        content_obj = MIMEText(send_content, 'plain', 'utf-8')  # 第一个参数为邮件内容
        message.attach(content_obj)

        # 构造附件
        att = MIMEText(_text=self._get_zip_file(), _subtype='base64', _charset='utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="{}"'.format(settings.SEND_FILE_NAME
                                                                        )  # # filename 为邮件附件中显示什么名字
        message.attach(att)

        try:
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtp_obj.login(mail_user, mail_pass)
            smtp_obj.sendmail(sender, receivers, message.as_string())
            smtp_obj.quit()
            logger().info('邮件发送成功')

        except smtplib.SMTPException as e:
            logger().error('email send error: {}'.format(e))
    def _get_zip_file(self):
        """ 获取zip文件内容 """
        with open(file=os.path.join(settings.BASE_DIR, 'report', 'allure_report.zip'), mode='rb') as f:
            return f.read()




if __name__ == '__main__':

    AllureOperate().get_allure_report()


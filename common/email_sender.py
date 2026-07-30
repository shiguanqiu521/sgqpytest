# -*- coding: utf-8 -*-
"""
@File    : email_sender.py
@Time    : 2026/7/29 16:35
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from loguru import logger
from config.settings import settings


class EmailSender:
    def __init__(self):
        self.sender = settings.MAIL_SENDER.strip()
        self.password = settings.MAIL_PASSWORD.strip()
        self.smtp_host = settings.MAIL_SMTP_HOST.strip()
        self.smtp_port = int(settings.MAIL_SMTP_PORT)

        # 环境变量已经解析为list，仅清洗空值和空格
        self.receivers = [item.strip() for item in settings.MAIL_RECEIVERS if item.strip()]
        self.cc_list = [item.strip() for item in settings.MAIL_CC if item.strip()]

    def _attach_file(self, msg, file_path):
        """附件绑定函数"""
        if not os.path.exists(file_path):
            logger.warning(f"附件不存在，跳过：{file_path}")
            return
        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = os.path.basename(file_path)
        part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
        msg.attach(part)

    def send_report_mail(self, pass_count, fail_count, skip_count, env, tag):
        subject = f"【自动化测试报告】环境:{env} | 标签:{tag} | 通过:{pass_count} 失败:{fail_count} 跳过:{skip_count}"
        html_content = f"""
        <h3>自动化测试执行结果</h3>
        <p>执行环境：{env}</p>
        <p>执行标签：{tag}</p>
        <p>✅ 通过用例：{pass_count}</p>
        <p>❌ 失败用例：{fail_count}</p>
        <p>⏭️ 跳过用例：{skip_count}</p>
        <p>测试JSON结果见附件</p>
        """

        msg = MIMEMultipart("mixed")
        msg["From"] = self.sender.strip()

        # 收件人
        to_list = self.receivers
        msg["To"] = ",".join(to_list)

        # 抄送：列表有有效地址才添加Cc头部
        cc_list_clean = self.cc_list
        if cc_list_clean:
            msg["Cc"] = ",".join(cc_list_clean)

        msg["Subject"] = subject
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        # =========重点改动：移除allure文件夹附件，只附加json结果文件
        try:
            self._attach_file(msg, settings.JSON_RESULT)
        except Exception as e:
            logger.warning(f"结果文件附件添加失败:{e}")

        log_file = os.path.join(settings.LOG_PATH, f"{datetime.now().strftime('%Y-%m-%d')}.log")
        if os.path.exists(log_file):
            self._attach_file(msg, log_file)

        try:
            server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            server.local_hostname = "localhost"
            server.login(self.sender, self.password)
            all_receiver = to_list + cc_list_clean
            logger.info(f"邮件接收列表：{all_receiver}")
            server.sendmail(self.sender, all_receiver, msg.as_string())
            server.quit()
            logger.success("✅ 测试报告邮件发送成功！")
        except Exception as err:
            logger.error(f"❌ 邮件发送失败：{err}")


email_sender = EmailSender()
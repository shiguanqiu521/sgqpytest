# -*- coding: utf-8 -*-
"""
@File    : setting.py
@Time    : 2026/7/29 16:07
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import os
from dotenv import load_dotenv
from loguru import logger

ENV = os.getenv("ENV", "test")
ENV_FILE = f"./config/{ENV}.env"

try:
    load_dotenv(ENV_FILE, encoding="utf-8")
    logger.info(f"加载环境配置文件：{ENV_FILE}")
except Exception as e:
    logger.error(f"环境文件加载失败: {e}")
    raise FileNotFoundError("环境配置文件不存在")

class Settings:
    # 接口基础配置
    BASE_URL = os.getenv("BASE_URL")
    TIMEOUT = int(os.getenv("TIMEOUT", 10))

    # 数据库
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER")
    DB_PWD = os.getenv("DB_PWD")
    DB_NAME = os.getenv("DB_NAME")

    # 报告路径
    REPORT_HTML = "./reports/html/report.html"
    ALLURE_RAW = "./reports/allure_raw"
    ALLURE_HTML = "./reports/allure_html"
    LOG_PATH = "./reports/logs"
    JSON_RESULT = "./reports/case_result.json"

    # 邮件配置
    MAIL_SENDER = os.getenv("MAIL_SENDER")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_SMTP_HOST = os.getenv("MAIL_SMTP_HOST")
    MAIL_SMTP_PORT = int(os.getenv("MAIL_SMTP_PORT", 465))
    MAIL_RECEIVERS = [addr.strip() for addr in os.getenv("MAIL_RECEIVERS", "").split(",") if addr.strip()]
    MAIL_CC = [addr.strip() for addr in os.getenv("MAIL_CC", "").split(",") if addr.strip()]
    MAIL_SUBJECT_PREFIX = os.getenv("MAIL_SUBJECT_PREFIX", "Pytest自动化测试报告")

settings = Settings()
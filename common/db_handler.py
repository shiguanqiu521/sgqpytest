# -*- coding: utf-8 -*-
"""
@File    : db_handler.py
@Time    : 2026/7/29 16:35
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import pymysql
from config.settings import settings
from common.log_util import log

class DBHandler:
    def __init__(self):
        self.conn = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PWD,
            database=settings.DB_NAME,
            charset="utf8mb4"
        )
        self.cursor = self.conn.cursor()

    def execute_sql(self, sql: str):
        log.info(f"执行SQL：{sql}")
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

def get_db():
    return DBHandler()
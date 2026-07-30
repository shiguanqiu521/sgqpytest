# -*- coding: utf-8 -*-
"""
@File    : log_util.py
@Time    : 2026/7/29 16:32
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
from loguru import logger
from config.settings import settings
import sys

logger.remove()

# 控制台输出
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}:{function}:{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# 按天分割日志文件，保留7天
logger.add(
    f"{settings.LOG_PATH}/{{time:YYYY-MM-DD}}.log",
    rotation="00:00",
    retention="7 days",
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

log = logger
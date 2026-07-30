# -*- coding: utf-8 -*-
"""
@File    : conftest.py
@Time    : 2026/7/29 16:36
@Author  : Your Name
@Version : 1.1
@Desc    : 全局fixture：登录、DB、日志
"""
import pytest
from common.api_request import api
from common.token_cache import token_cache
from common.log_util import log
from common.db_handler import get_db


# 全局session前置：登录获取token（失败时降级）
@pytest.fixture(scope="session", autouse=True)
def global_login():
    log.info("===== 全局前置：登录获取Token =====")
    try:
        login_resp = api.send("POST", "/post", data={"username": "test_user", "password": "123456"})
        token = login_resp.json().get("args", {}).get("username")
        token_cache.set_token(token)
    except Exception as e:
        log.warning(f"全局登录失败，降级处理：{e}")
    yield
    log.info("===== 全局后置：全部用例执行结束 =====")


# 每条用例前后执行，自动创建/关闭数据库连接（连接失败时降级）
@pytest.fixture(scope="function", autouse=True)
def case_fixture(request):
    case_name = request.function.__name__
    log.info(f"\n========== 执行用例：{case_name} ==========")
    try:
        db = get_db()
        yield db
        db.close()
    except Exception as e:
        log.warning(f"数据库连接失败，跳过DB操作：{e}")
        yield None
    log.info(f"========== {case_name} 执行完毕 ==========\n")


# 全局读取Excel全部用例
@pytest.fixture(scope="session")
def all_case_data():
    from common.excel_handler import excel_handler
    return excel_handler.read_case("./data/api_cases.xlsx", "login")
# -*- coding: utf-8 -*-
"""
@File    : test_login.py
@Time    : 2026/7/29 16:36
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import pytest
from common.api_request import api
from common.assert_util import assert_util
from common.excel_handler import excel_handler

all_cases = excel_handler.read_case("./data/api_cases.xlsx", "login")
smoke_cases = excel_handler.filter_by_tag(all_cases, "smoke")
regress_cases = excel_handler.filter_by_tag(all_cases, "regress")
regress_param = excel_handler.get_param_pair(regress_cases)

class TestLogin:
    @pytest.mark.smoke
    def test_login_smoke(self):
        """冒烟正向登录用例"""
        case = smoke_cases[0]
        resp = api.send(
            method=case["method"],
            path=case["path"],
            data=eval(case["json_data"]) if case["json_data"] else None
        )
        assert_util.equal(resp.status_code, int(case["expect_code"]))
        assert_util.json_path(resp.json(), case["expect_json"], case["case_desc"])

    @pytest.mark.parametrize("case", regress_param)
    @pytest.mark.regress
    def test_login_regress(self, case):
        """批量反向参数化用例"""
        resp = api.send(
            method=case["method"],
            path=case["path"],
            data=eval(case["json_data"]) if case["json_data"] else None
        )
        assert_util.equal(resp.status_code, int(case["expect_code"]))
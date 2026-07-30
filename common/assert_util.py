# -*- coding: utf-8 -*-
"""
@File    : assert_util.py
@Time    : 2026/7/29 16:34
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
from common.log_util import log

class AssertUtil:
    @staticmethod
    def equal(actual, expect, msg="数值不相等"):
        log.info(f"等值断言：实际={actual} 预期={expect}")
        assert actual == expect, f"{msg} 实际:{actual},预期:{expect}"

    @staticmethod
    def contains(actual: str, expect: str, msg="文本不包含"):
        log.info(f"包含断言：{actual} 包含 {expect}")
        assert expect in actual, f"{msg} 文本:{actual},需包含:{expect}"

    @staticmethod
    def not_null(val, msg="值为空"):
        assert val is not None and str(val).strip() != "", msg

    @staticmethod
    def json_path(json_data: dict, path: str, msg=""):
        """
        校验JSON路径值，path格式: key1.key2.expected_value
        如: args.username.test_user 表示校验 data["args"]["username"] == "test_user"
        """
        keys = path.split(".")
        expect_val = keys[-1]
        json_keys = keys[:-1]
        temp = json_data
        for k in json_keys:
            temp = temp.get(k, None)
        log.info(f"JSON路径{".".join(json_keys)} 实际:{temp},预期:{expect_val} | {msg}")
        assert str(temp) == expect_val, f"JSON校验失败，路径{".".join(json_keys)} 实际:{temp},预期:{expect_val} | {msg}"

assert_util = AssertUtil()
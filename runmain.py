# -*- coding: utf-8 -*-
"""
@File    : runmain.py
@Time    : 2026/7/29 16:05
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import os
import sys
import json
import pytest
from config.settings import settings
from common.log_util import log
from common.email_sender import email_sender

def run():
    env = sys.argv[1] if len(sys.argv) > 1 else "test"
    tag = sys.argv[2] if len(sys.argv) > 2 else "smoke"
    os.environ["ENV"] = env
    log.info(f"===== 自动化框架启动｜环境：{env}｜执行标签：{tag} =====")

    # 创建报告目录
    dirs = [settings.ALLURE_RAW, settings.ALLURE_HTML, os.path.dirname(settings.REPORT_HTML), settings.LOG_PATH]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

    args = [
        "./testcase",
        "-v",
        "-n", "2",
        "-m", tag,
        "--html", settings.REPORT_HTML,
        "--self-contained-html",
        "--alluredir", settings.ALLURE_RAW,
        "--json-report", "--json-report-file", settings.JSON_RESULT
    ]
    exit_code = pytest.main(args)

    # 精准统计成功/失败/跳过用例
    pass_count = fail_count = skip_count = 0
    if os.path.exists(settings.JSON_RESULT):
        with open(settings.JSON_RESULT, "r", encoding="utf-8") as f:
            res_data = json.load(f)
        for case in res_data["tests"]:
            status = case["outcome"]
            if status == "passed":
                pass_count += 1
            elif status == "failed":
                fail_count += 1
            elif status == "skipped":
                skip_count += 1

    # 执行完成自动推送邮件
    email_sender.send_report_mail(pass_count, fail_count, skip_count, env, tag)

    # 已装好Java+allure再取消下面两行注释
    # os.system(f"allure generate {settings.ALLURE_RAW} -o {settings.ALLURE_HTML} --clean")
    # os.system(f"allure open {settings.ALLURE_HTML}")

    return exit_code

if __name__ == "__main__":
    code = run()
    sys.exit(code)
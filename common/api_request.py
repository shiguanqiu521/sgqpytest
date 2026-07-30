# -*- coding: utf-8 -*-
"""
@File    : api_request.py
@Time    : 2026/7/29 16:33
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import requests
from common.log_util import log
from common.token_cache import token_cache
from config.settings import settings
from functools import wraps

def retry(times=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    log.warning(f"接口第{i+1}次请求失败：{e}")
                    if i == times - 1:
                        raise e
            return None
        return wrapper
    return decorator

class ApiRequest:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = settings.BASE_URL
        self.timeout = settings.TIMEOUT

    @retry(times=2)
    def send(self, method, path, data=None, params=None, headers=None, files=None):
        url = self.base_url + path
        req_headers = {"Content-Type": "application/json"}
        if token_cache.get_token():
            req_headers["Authorization"] = f"Bearer {token_cache.get_token()}"
        if headers:
            req_headers.update(headers)

        log.info(f"===== 发起请求 =====")
        log.info(f"地址：{url}")
        log.info(f"方式：{method}")
        log.info(f"请求头：{req_headers}")
        log.info(f"请求体：{data if data else params}")

        resp = self.session.request(
            method=method.upper(),
            url=url,
            json=data,
            params=params,
            headers=req_headers,
            files=files,
            timeout=self.timeout
        )
        log.info(f"状态码：{resp.status_code}")
        log.info(f"响应：{resp.text}")
        log.info(f"====================\n")
        return resp

api = ApiRequest()
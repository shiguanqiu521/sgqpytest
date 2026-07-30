# -*- coding: utf-8 -*-
"""
@File    : token_cache.py
@Time    : 2026/7/29 16:33
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
class TokenCache:
    _instance = None
    token = ""

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_token(self, token):
        self.token = token

    def get_token(self):
        return self.token

token_cache = TokenCache()
# -*- coding: utf-8 -*-


class Tenant(object):
    def __init__(self, user, url, token):
        self.hive_user = user
        self.hive_api_token = token
        self.hive_api_url = url

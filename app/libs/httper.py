"""
 Created by ldh on 19-12-12
"""
__author__ = "刘大怪"

import requests


# 封装 http 请求
class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''

        return r.json() if return_json else r.text

        # 下面是低级方式
        # if r.status_code == 200:
        #     if return_json:
        #         return r.json()
        #     else:
        #         return r.text
        # else:
        #     if return_json:
        #         return {}
        #     else:
        #         return ''

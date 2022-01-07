"""
本插件用于从https://www.tianqiapi.com/ 获取天气数据
    不提供API 链接,请自己去获取
"""

import json
import sys
import time
import re

import requests


# 发送get请求获取信息
def request_data(request_params: dict) -> dict:
    try:
        _data = requests.get(url=get_api(), params=request_params, timeout=8).json()
    except requests.exceptions.ConnectTimeout as t:
        return {'Connect timed out!': t.errno}
    except requests.exceptions.HTTPError as h:
        return {'HTTP error!': h.errno}
    except requests.exceptions.ReadTimeout as r:
        return {'Read timed out': r.errno}

    return _data


# 从./data/weather_query/config.json中获取api链接
def get_api() -> str:
    try:
        with open('./data/weather_query/config.json', 'r', encoding='utf-8') as fp:
            cfg = json.load(fp)
            if cfg['url'] == 0 or cfg['url'] == "":
                print("要在\\data\\wether_query\\config.json中填写请求地址哟~\n")
                time.sleep(0.5)
                sys.exit()
    except FileNotFoundError:
        with open('./data/weather_query/config.json', 'w', encoding='utf-8') as fp:
            _dict = {
                "name": "weather_query",
                "url": ""
            }
            json.dump(_dict, fp, indent=4, ensure_ascii=False)
            print("要在\\data\\wether_query\\config.json中填写请求地址哟~\n")
            time.sleep(0.5)
            sys.exit()
    return cfg['url']


# 筛选整理请求参数
def format_data(param: str = '') -> dict:
    cityname = re.compile("[\u4e00-\u9fa5]{2,9}")
    cityid = re.compile("\d{9}")
    ip = re.compile("((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)")
    params = {
        "cityid": '',
        "city": '',
        "ip": ''
    }
    city_data = dict()
    if cityname.fullmatch(param) and param[-1] != '市' and param[-1] != '区':
        params['city'] = param
    elif cityid.fullmatch(param):
        params['cityid'] = param
    elif ip.fullmatch(param):
        params['ip'] = param
    else:
        params = {
            "cityid": " "
        }
    city_data = request_data(params)

    return city_data


if __name__ == "__main__":
    x = input("输入查询参数: ")
    print(request_data({"cityname": 54616}))

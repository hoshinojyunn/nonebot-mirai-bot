"""
getdata.py-本模块用于获取中央气象台天气预报的json响应数据
"""
import json
import re

import requests

base_url = 'http://www.nmc.cn/rest/weather'
header = {
    'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
}


# 获取城市对应的stationid
def get_stationid(cityname: str) -> str:
    with open("./src/plugins/weather_forcast/stationid/city_code.json", 'r') as fp:
        city = json.load(fp)
    return city[cityname]


# 正则筛,整理参数
def format_data(param: str = '') -> dict:
    city_name = re.compile("[\u4e00-\u9fa5]{2,10}")
    station_id = re.compile("\d{5}")
    params: dict[str, str] = {
        'stationid': 'none'
    }

    if city_name.fullmatch(param):
        if param[-1] == '市' or param[-1] == '区':
            param = param[0:-1]

        params['stationid'] = get_stationid(param)
    elif station_id.fullmatch(param):
        params['stationid'] = param

    return params


# 发送get请求
def request_data(param: str) -> dict:
    try:
        weather_data = requests.get(url=base_url, headers=header, params=format_data(param), timeout=5).json()
    except requests.exceptions.ConnectTimeout as cto:
        return {'Connect timed out!': cto.errno}
    except requests.exceptions.HTTPError as he:
        return {'HTTP error!': he.errno}
    except requests.exceptions.ReadTimeout as rto:
        return {'Read timed out': rto.errno}

    return weather_data


if __name__ == "__main__":
    x = input("in:")
    r = json.dumps(request_data(x), ensure_ascii=False, indent=4)
    with open("测试数据4.json", 'w') as f:
        f.write(r)

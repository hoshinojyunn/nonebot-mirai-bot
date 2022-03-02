#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
import json
import sys
import os

import nonebot
from nonebot.adapters.mirai import WebsocketBot


def main():
    nonebot.init()
    # config = nonebot.get_driver().config
    app = nonebot.get_asgi()
    driver = nonebot.get_driver()
    driver.register_adapter("mirai-ws", WebsocketBot, qq=get_qq("mirai-ws"))
    nonebot.load_builtin_plugins()  # 加载nonebot内置插件

    nonebot.load_plugins('./src/plugins')
    nonebot.load_plugins('./src/plugins/weather_query')  # 加载插件
    nonebot.load_plugins('./src/plugins/spider-master')
    nonebot.load_plugins('./src/plugins/EroPics')
    nonebot.load_plugins('./src/plugins/bf1')
    nonebot.run()


# nonebot.load_from_toml("pyproject.toml")

# Modify some config / config depends on loaded configs
#
# config = driver.config
# do something...

def get_qq(connect_type: str):
    try:
        with open('exconfig.json', 'r', encoding='utf-8') as fp:
            obj = json.load(fp)
            if obj[connect_type]['qq'] == 0:
                print('请于exconfig.json中填写qq号\n')
                sys.exit()
    except FileNotFoundError:
        remake_exconfig(connect_type)
        print('请于exconfig.json中填写qq号\n')
        sys.exit()
    return obj[connect_type]['qq']


def remake_exconfig(connect_type: str):
    with open('exconfig.json', 'w', encoding='utf-8') as fp:
        dict = {
            '说明': '本文件为用于补充部分特殊配置的文件，不会被push至远端git库',
            connect_type: {'qq': 0}
        }
        json.dump(dict, fp, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # 临时启动mcl
    #os.system('cd Mirai_base && start mcl.cmd')

    main()

    nonebot.logger.warning(app="Should use `nb run` to start the bot instead of manually running!")

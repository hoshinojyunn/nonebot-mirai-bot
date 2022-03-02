import json

import requests
from nonebot import on_command
from nonebot.adapters.mirai import Bot, MessageEvent
from pathlib import Path


def getWeaponData(name: str) -> str:
    all_data: dict
    weapon_data: list
    message:str = ''
    try:
        r = requests.get(url="https://api.gametools.network/bf1/weapons/",
                         params={"format_values": "true", "name": name, "platform": "pc", "lang": "en-us"})
        r.raise_for_status()
        all_data = r.json()
        userName = all_data.get("userName")
        message += userName + '的十大最佳武器与击杀数:' + '\n'
        # weapons为一个列表
        weapon_data = all_data["weapons"]
        print(type(weapon_data))
        # weapons内元素均为字典
        data = sorted(weapon_data, key=lambda i: i['kills'], reverse=True)
        for i in range(0, 10):
            message += str(i + 1) + "." + data[i].get('weaponName') + ":" + str(data[i].get('kills')) + "\n"
        print(message)
        return message
    except:
        return "input name isn't exist"


def bf1_get_name(qq: str) -> str:
    # 取得当前程序文件的路径
    path = (Path(__file__).resolve() / '../connect.json').resolve()
    try:
        with open(path, 'r') as f:
            return json.load(f)[qq]
    except:
        return ''


bf1 = on_command('bf1')
bf1_help = on_command(('bf1', 'help'))
help_message = "/bf1查询帮助,如下:\n/bf1.set [橘子名]，绑定你的qq号与橘子账户名\n/bf1.weapon，查询你的最佳武器与击杀。"

@bf1.handle()
@bf1_help.handle()
async def send_help(bot: Bot, event: MessageEvent):
    await bot.send(event, help_message, at_sender=True)



bf1_finding = on_command(cmd=('bf1', 'weapon'))


@bf1_finding.handle()
async def bf1_send_data(bot: Bot, event: MessageEvent):
    user_qq = event.get_user_id()
    user_name = bf1_get_name(user_qq)
    if user_name != '':
        await bot.send(event, getWeaponData(user_name), at_sender=True)
    else:
        await bot.send(event, "查询失败", at_sender=True)

if __name__ == "__main__":
    getWeaponData("owndevice")
    
    

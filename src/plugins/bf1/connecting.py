"""
用于添加qq号与名字对应的json项
"""
import json
import os
from nonebot import on_command, on_keyword
from nonebot.adapters.mirai import Bot, MessageEvent
from pathlib import Path

set_name = on_command(cmd=('bf1', 'set'))
test = on_command(cmd=("test3","run"))


@test.handle()
async def testing(bot: Bot, event: MessageEvent):
    await bot.send(event, "test成功")


@set_name.handle()
async def add_player(bot: Bot, event: MessageEvent):
    j_dict:dict
    text = event.get_plaintext()
    text_list = text.split()
    name = text_list[0] if text_list else ''  # 获得名字
    path = (Path(__file__).resolve() / '../connect.json').resolve()
    if not path.is_file():
        if not path.parent.is_dir():
            os.makedirs(path.parent)
        open(path, 'w').close()
    message = "操作失败"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            j_dict = json.load(f)
        with open(path, 'w', encoding='utf-8') as f:
            if name != '':
                j_dict[event.get_user_id()] = name
                message = "绑定成功: " + name
            elif name == '' and event.get_user_id() in j_dict:
                j_dict.pop(event.get_user_id())
                message = "清除成功"
            json.dump(j_dict, f)
    except Exception as e:
        message = "操作失败"
    finally:
        await bot.send(event, message, at_sender=True)



if __name__ == "__main__":
    testing()
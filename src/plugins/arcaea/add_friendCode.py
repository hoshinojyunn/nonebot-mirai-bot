"""
用于添加qq号与好友码对应的json项
"""
import json
import os
from nonebot import on_keyword
from nonebot.adapters.mirai import Bot, MessageEvent

add_p = on_keyword({'加入'})
# test = on_keyword({"test1"})
#
#
# @test.handle()
# async def test(bot: Bot, event: MessageEvent):
#     id = event.get_user_id()
#     await bot.send(event, id, at_sender=False)


@add_p.handle()
async def add_player(bot: Bot, event: MessageEvent):
    text = event.get_plaintext()
    text_list = text.split()
    friend_code = text_list[1]  # 获得好友码
    json_path = os.path.join(os.getcwd(), 'src', 'plugins', 'arcaea', 'detail.json')
    with open(json_path, 'r') as f:
        j_dict = json.load(f)
    with open(json_path, 'w') as f:
        j_dict[event.get_user_id()] = friend_code
        json.dump(j_dict, f)
    await bot.send(event, "添加成功", at_sender=True)


if __name__ == "__main__":
    json_path = os.path.join(os.getcwd(), 'detail.json')
    with open(json_path, 'r', encoding="utf-8") as f:
        j_dict = json.load(f)
    print(j_dict, type(j_dict))

from nonebot import on_keyword
from nonebot.adapters.mirai import Bot, MessageEvent, MessageSegment, MessageChain
import requests


# https://api.yimian.xyz/img
class Get_setu():
    def __init__(self):
        self.session = requests.session()

    def get_pic(self) -> list:  # 全年龄
        response1 = requests.get(url="https://api.nyan.xyz/httpapi/sexphoto/",
                                 params={"num": 1, "r18": True}, timeout=30).json()
        result = response1.get('data')
        return result.get('url')

    def get_super_pic(self) -> list:  # r18
        response2 = requests.get(url="https://api.nyan.xyz/httpapi/sexphoto/",
                                 params={"num": 1, "r18": "true"}, timeout=30).json()
        result = response2.get('data')
        return result.get('url')


def merge_pics() -> MessageChain:
    get = Get_setu()
    pics_url = get.get_pic()
    chain = MessageChain()
    for link in pics_url:
        chain.append(MessageSegment.image(image_id=None, url=link, path=None))
    return chain


def merge_super_pics() -> MessageChain:
    get = Get_setu()
    _url = get.get_super_pic()
    _chain = MessageChain("lsp,注意身体")
    for link in _url:
        _chain.append(MessageSegment.image(image_id=None, url=link, path=None))
    return _chain


# http://api.mtyqx.cn/api/random.php
Pic = on_keyword({'随机色图'}, priority=3)


@Pic.handle()
async def get_pics(bot: Bot, event: MessageEvent):
    await bot.send(event, merge_pics(), at_sender=False)


Super_pic = on_keyword({'超级色图'}, priority=3)


@Super_pic.handle()
async def get_super_pics(bot: Bot, event: MessageEvent):
    await bot.send(event, merge_super_pics(), at_sender=False)


test = on_keyword({'setu'}, priority=3)


@test.handle()
async def test(bot: Bot, event: MessageEvent):
    mess = MessageSegment.image(image_id=None, url="https://api.yimian.xyz/img", path=None)
    await bot.send(event, mess)


if __name__ == "__main__":
    get = Get_setu()
    _url = get.get_super_pic()
    _chain = MessageChain("lsp,注意身体")
    for link in _url:
        _chain.append(MessageSegment.image(image_id=None, url=link, path=None))

from nonebot import on_keyword, on_command
from nonebot.adapters.mirai import Bot, MessageEvent, MessageSegment, MessageChain
import requests


# https://api.yimian.xyz/img
class Get_setu():
    def __init__(self):
        self.session = requests.session()

    def get_pic(self) -> list:  # 全年龄
        response1 = requests.get(url="https://api.nyan.xyz/httpapi/sexphoto/",
                                 params={"num": 1}, timeout=30).json()
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
    chain = MessageChain('')
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

setu = on_command('Setu')
setu_help = on_command(('Setu','help'))


@setu.handle()
@setu_help.handle()
async def setu_help(bot: Bot, event: MessageEvent):
    help_message = '发送 [随机色图]: 返回一张普通setu\n发送 [超级色图]: 返回一张r18 setu(慎用)'
    await bot.send(event, help_message, True)


# http://api.mtyqx.cn/api/random.php
Pic = on_keyword({'随机色图'}, priority=2)


@Pic.handle()
async def get_pics(bot: Bot, event: MessageEvent):
    await bot.send(event, "随机色图正在路上......", at_sender=True)
    try:
        pics = merge_pics()
        await bot.send(event, pics, at_sender=True)
    except requests.exceptions.ReadTimeout:
        await bot.send(event, "响应超时,大概是API炸了", True)


Super_pic = on_keyword({'超级色图'}, priority=2)


@Super_pic.handle()
async def get_super_pics(bot: Bot, event: MessageEvent):
    await bot.send(event, "超级色图正在路上......", at_sender=True)
    try:
        pics = merge_super_pics()
        await bot.send(event, pics, at_sender=True)
    except requests.exceptions.ReadTimeout:
        await bot.send(event, "响应超时,大概是API炸了", True)


test = on_command(cmd=('test', 'b30'), priority=2)


@test.handle()
async def test(bot: Bot, event: MessageEvent):
    pic = MessageSegment.image(path='间桐樱1.jpg')
    await bot.send(event, pic, at_sender=False)


if __name__ == "__main__":
    get = Get_setu()
    _url = get.get_super_pic()
    _chain = MessageChain("lsp,注意身体")
    for link in _url:
        _chain.append(MessageSegment.image(image_id=None, url=link, path=None))

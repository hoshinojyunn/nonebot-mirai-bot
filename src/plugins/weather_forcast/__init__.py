"""
本插件用于从www.nmc.cn(中央气象台)获取各城市的天气情况查询
"""

from . import format_message
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.adapters.mirai import Bot, MessageEvent, MessageSegment,MessageChain

weather_test = on_command(cmd="weather", rule=to_me(), priority=2)


@weather_test.handle()
async def get_message_cmd(bot: Bot, event: MessageEvent):
    args = str((event.get_message())).strip()
    await bot.send(event, format_message.SendMessage(args).text_message(), at_sender=True)








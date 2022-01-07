"""
用于测试的复读插件
"""

from nonebot.plugin import on_keyword, on_command
from nonebot.rule import to_me
from nonebot.adapters.mirai import Bot, MessageEvent

txt = on_keyword({'rua'}, rule=to_me())


@txt.handle()
async def send_txt(bot: Bot, event: MessageEvent):
    text = event.get_message()
    await bot.send(event, text, at_sender=False)


command_test = on_command('echo')


@command_test.handle()
async def _echo(bot: Bot, event: MessageEvent):
    text = event.get_plaintext()
    await bot.send(event, text, at_sender=True)

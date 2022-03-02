from nonebot.plugin import on_keyword, on_command
from nonebot.rule import to_me
from nonebot.adapters.mirai import Bot, MessageEvent


help_message = '/gal:查看gal模块的帮助\n/Setu(注意大小写):查看setu模块的帮助\n/bf1:查看bf1模块的帮助'

total_help = on_command('total_help')




@total_help.handle()
async def send_help(bot: Bot, event: MessageEvent):
    await bot.send(event, help_message, at_sender=False)
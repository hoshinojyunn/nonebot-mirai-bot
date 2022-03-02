# from nonebot import on_command, on_keyword
# from nonebot.adapters.mirai import Bot, MessageEvent



# bf1 = on_command('bf1')
# bf1_help = on_command(('bf1', 'help'))
# help_message = "/bf1查询帮助,如下:\n/bf1.set [橘子名]，绑定你的qq号与橘子账户名\n/bf1.weapon，查询你的最佳武器与击杀。"


# @bf1.handle()
# @bf1_help.handle()
# async def send_help(bot: Bot, event: MessageEvent):
#     await bot.send(event, help_message, at_sender=True)
from nonebot.plugin import on_command, on_keyword
from nonebot.rule import to_me
from nonebot.adapters.mirai import Bot, MessageEvent, Event, MessageSegment, MessageChain

State = {}  # 初始功能dict
matcher = on_keyword({"test"}, priority=3, rule=to_me())


# @matcher.args_parser
# async def parse(bot: Bot, event: Event, state: dict):
#     print(state["_current_key"], ":", str(event.get_message()))
#     state[state["_current_key"]] = str(event.get_message())  # 查命令


@matcher.handle()
async def first_receive(bot: Bot, event: Event):
    ater_id = event.get_user_id()
    await bot.send(event, ater_id, at_sender=False)

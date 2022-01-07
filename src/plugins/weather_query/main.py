"""
基于:https://www.tianqiapi.com/
失败的插件
"""

import getdata

from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.adapters.mirai import Bot, MessageEvent, MessageSegment, MessageChain


# 图片与文本消息合并
def message_finishing(param: str) -> MessageSegment:
    _data = getdata.format_data(param)
    return image_message(_data) + MessageSegment.plain(text_message(_data))


def message_merge(param: str) -> MessageChain:
    _data = getdata.format_data(param)

    text_1 = MessageSegment.plain(text_message(_data))
    text_2 = MessageSegment.plain("")
    message = MessageChain([text_1, text_2])

    return message


# 整理要发送的文本消息
def text_message(city_data: dict) -> str:
    air_quality = ''

    # str
    if 'errcode' in city_data:
        if city_data['errcode'] == 100 and city_data['errmsg'] == '仅限国内城市天气!':
            return "参数看不懂啦~ \n请输入纯中文,不要带'市'和'区'\n(支持市区县, 不支持乡镇级别)"
        elif city_data['errmsg'][0:7] == 'city不存在':
            return "你到底想查哪里啦~"
        else:
            return "呃呃,你想查什么天气?"
    elif 'Connect timed out!' in city_data:
        return f'连接超时了呢...{city_data["Connect timed out!"]}'
    elif 'HTTP error!' in city_data:
        return f'HTTP error..{city_data["HTTP error!"]}'
    elif 'Read timed out' in city_data:
        return f"Read timed out..{city_data['Read timed out']}"
    else:

        if 0 <= eval(city_data['air']) <= 50:
            air_quality = '一级（优）空气质量令人满意，基本无空气污染'
        elif 51 <= eval(city_data['air']) <= 100:
            air_quality = '二级（良）空气质量可接受，但某些污染物可能对极少数异常敏感人群健康有较弱影响'
        elif 101 <= eval(city_data['air']) <= 150:
            air_quality = '三级（轻度污染）易感人群症状有轻度加剧，健康人群出现刺激症状'
        elif 151 <= eval(city_data['air']) <= 200:
            air_quality = '四级（中度污染）进一步加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响'
        elif 201 <= eval(city_data['air']) <= 300:
            air_quality = '五级（重度污染）心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状'
        elif 300 <= eval(city_data['air']):
            air_quality = '六级（严重污染）健康人群运动耐受力降低，有明显强烈症状，提前出现某些疾病'

        return f"\n现在 {city_data['city']} 的天气是 {city_data['wea']} 哟~\n" \
               f"温度是 {city_data['tem']}℃\n" \
               f"白天温度:{city_data['tem_day']}℃,夜晚温度:{city_data['tem_night']}℃\n" \
               f"风向: {city_data['win']}\n" \
               f"风力等级:{city_data['win_speed']}, 风速:{city_data['win_meter']}\n" \
               f"空气质量:{city_data['air']} {air_quality}\n" \
               f"[数据更新时间:{city_data['update_time']}]"


# 图片消息
def image_message(city_data: dict) -> MessageSegment:
    # 图片
    # 根据api:9种固定:xue、lei、shachen、wu、bingbao、yun、yu、yin、qing
    path = f"../../../../data/weather_query/icon/{city_data['wea_img']}.png"
    return MessageSegment.image(path=path)


weather_cmd = on_command(cmd="天气", rule=to_me(), priority=3)


@weather_cmd.handle()
async def get_message_cmd(bot: Bot, event: MessageEvent):
    args = str((event.get_message())).strip()
    await bot.send(event, message_merge(args), at_sender=True)

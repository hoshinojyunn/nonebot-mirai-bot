"""
format_message.py-本模块用于将json格式的响应进一步处理,打包成MessageSegment
"""

from . import getdata


class SendMessage(object):
    # 原始数据
    _city_data = {}
    # data部分
    weather_data = {}

    # 初始化获取数据

    def __init__(self, city_name: str):
        self._city_data = getdata.request_data(city_name)
        self.weather_data = self._city_data['data']

    def test(self):
        return f"{self.weather_data['real']['weather']['info']}"

    # 整理文本消息

    def text_message(self) -> str:
        aqidict = [{},
                   {'level': '优', 'health': '空气质量令人满意,基本无空气污染。', 'suggestion': '各类人群可正常活动。'},
                   {'level': '良', 'health': '空气质量可接受,但某些污染物可能对极少数异常,敏感人群健康有较弱影响。',
                    'suggestion': '极少数异常敏感人群应减少户外活动。'},
                   {'level': '轻度污染', 'health': '易感人群症状有轻度加剧,健康人群出现刺激症状。',
                    'suggestion': '儿童、老年人及心脏病、呼吸系统疾病患者应减少长时间、高强度的户外锻炼。'},
                   {'level': '中度污染', 'health': '进一步加剧易感人群症状,可能对健康人群心脏、呼吸系统有影响。',
                    'suggestion': '儿童、老年人及心脏病、呼吸系统疾病患者避免长时间、高强度的户外锻炼,一般人群适量减少户外运动。'},
                   {'level': '重度污染', 'health': '心脏病和肺病患者症状显著加剧,运动耐受力减低,健康人群普遍出现症状。',
                    'suggestion': '老年人和心脏病、肺病患者应停留在室内，停止户外活动，一般人群减少户外活动。'},
                   {'level': '严重污染', 'health': '健康人运动耐力减低,有显著强烈症状,提前出现某些疾病。',
                    'suggestion': '老年人和病人应当留在室内，避免体力消耗，一般人群应避免户外活动。'}
                   ]
        icomfort = {
            9999: '-',
            4: '很热，极不适应',
            3: '热，很不舒适',
            2: '暖，不舒适',
            1: '温暖，较舒适',
            0: '舒适，最可接受',
            -1: '凉爽，较舒适',
            -2: '凉，不舒适',
            -3: '冷，很不舒适',
            -4: '很冷，极不适应',
        }

        return f"\n现在 {self.weather_data['real']['station']['city']} 的天气是 {self.weather_data['real']['weather']['info']} !\n" \
               f"气温是 {self.weather_data['real']['weather']['temperature']}℃ 体感温度:{self.weather_data['real']['weather']['temperature']}℃\n" \
               f"温差: {self.weather_data['real']['weather']['temperatureDiff']}℃\n" \
               f"气压: {self.weather_data['real']['weather']['airpressure']}hPa\n" \
               f"风向: {self.weather_data['real']['wind']['direct']} 风力: {self.weather_data['real']['wind']['power']}\n" \
               f"相对湿度: {self.weather_data['real']['weather']['humidity']}% 降水量: {self.weather_data['real']['weather']['rain']}mm\n" \
               f"舒适度: {icomfort[self.weather_data['real']['weather']['icomfort']]}\n" \
               f"空气质量: {aqidict[self.weather_data['air']['aq']]['level']}, {aqidict[self.weather_data['air']['aq']]['health']}\n" \
               f"[发布时间: {self.weather_data['real']['publish_time']}]"


if __name__ == "__main__":
    r = SendMessage('北京')
    print(r.weather_data['real']['weather']['info'])
    print(r.test())
    print()

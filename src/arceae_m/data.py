"""
ArcData 支持模块
"""

import json
from copy import deepcopy
from typing import Dict

import brotli
from websocket import WebSocketApp

import arceae_m.exception as exception
import arceae_m.paint_catch
get_song_pic_url = arceae_m.paint_catch.get_song_pic_url


# __all__ = ['ArcData']

class ArcData:
    """
    ArcData类，对应一个用于查询和保存单个玩家数据的数据包模型

    本类中所有返回 `dict` 或 `str` 的方法返回 `{}` 或 `""` 时，表示方法失败，请注意判断

    * 使用 catch_data 方法向服务器获取数据[很慢]
    * 使用 get 前缀的方法在获取数据后查询对应信息
    """
    _url: str = 'wss://arc.estertion.win:616/'
    # 使用的后端服务器 websocket 地址
    __friend_code: str
    # 好友码
    __raw_data: Dict

    # 原始数据

    def __init__(self, friend_code: str) -> None:
        """
        * `friend_code`: 被查询玩家的 Arceae 好友码，会被存储在该对象中
        """
        self.__friend_code = '0'
        self.__raw_data = {}
        self.set_friend_code(friend_code)

    def check_friend_code(self) -> bool:
        """
        简单检查该 ArcData 对象绑定的好友码，返回检查结果

        通过该检查不代表好友码一定合法
        """
        friend_code = self.__friend_code
        if friend_code.isdigit() and len(friend_code) == 9:
            return True
        return False

    def set_friend_code(self, friend_code: str) -> bool:
        """
        设置该 ArcData 对象绑定的好友码，返回成功状态

        * `friend_code`: 被查询玩家的 Arceae 好友码，会被存储在该对象中
        """
        if friend_code.isdigit() and len(friend_code) == 9:
            self.__friend_code = friend_code
            return True
        return False

    def catch_data(self, on_receive=None) -> None:
        """
        从服务器获取玩家数据并存储在该对象中.

        非常慢，建议异步处理
        """
        try:
            if not self.__friend_code:
                return
            self.__raw_data.clear()
            ans = {
                'songs': {},
                'userinfo': {},
                'scores': []
            }

            def on_open(app: WebSocketApp):
                app.send(self.__friend_code)

            def on_message(app: WebSocketApp, message):
                if isinstance(message, bytes):
                    message = json.loads(brotli.decompress(message))

                    def song_title(message: Dict[str, dict]):
                        for key, val in message['data'].items():
                            if key not in ans['songs']:
                                ans['songs'][key] = {}
                            ans['songs'][key]['title'] = val

                    def song_artist(message):
                        for key, val in message['data'].items():
                            if key not in ans['songs']:
                                ans['songs'][key] = {}
                            ans['songs'][key]['artist'] = val

                    def user_info(message):
                        ans['userinfo'] = message['data']

                    def scores(message):
                        ans['scores'] += message['data']

                    def lookup_result(message):
                        print('resv lookup_result')
                        print(message)

                    def constants(message):
                        print('resv constants')
                        print(message)

                    def default_case(message):
                        print('resv defalut_case')
                        print(message)

                    def switch(message):
                        dic = {
                            'songtitle': song_title,
                            'songartist': song_artist,
                            'userinfo': user_info,
                            'scores': scores,
                            'lookup_result': lookup_result,
                            'constants': constants
                        }
                        dic.get(message['cmd'], default_case)(message)

                    switch(message)
                elif isinstance(message, str):
                    if message == 'queried' and on_receive is not None:
                        try:
                            on_receive()
                        except Exception as e:
                            raise e
                    if message == 'queued' or 'bye':
                        pass
                    elif message == 'invalid cmd':
                        raise exception.ArceaeQueryFailed(self, 'invalid cmd')
                    else:
                        print('UNKNOW MESSAGE: ', message)
                else:
                    raise Exception('Unknow error: illegal message')

            def on_error(app: WebSocketApp, e: Exception):
                raise exception.ArceaeQueryFailed(self, e)

            def on_close(app: WebSocketApp, status_code, close_msg):
                pass

            app = WebSocketApp(
                self._url,
                on_open=on_open,
                on_message=on_message,
                on_close=on_close,
                on_error=on_error)
            app.run_forever()
            self.__raw_data = ans
        except exception.ArceaeBaseException as e:
            raise e
        except Exception as e:
            raise exception.ArceaeQueryFailed(self, e)

    def has_data(self) -> bool:
        """
        返回该 ArcData 对象是否存储了玩家数据
        """
        return len(self.__raw_data) > 0

    def get_raw_data(self) -> dict:
        """
        获取该对象保存的数据的副本
        """
        if self.has_data():
            return deepcopy(self.__raw_data)
        else:
            return {}

    def get_song_paint(self, song_id: str) -> str:
        """
        返回曲绘的 URL 地址

        该方法不需要在 `catch_data` 后执行

        * `song_id`: 曲目id，为英文字符组成的字符串
        """
        return get_song_pic_url(song_id)

    def get_songs_dict(self) -> dict:
        """
        获取曲目表的字典
        """
        if self.has_data():
            try:
                return self.__raw_data['songs']
            except Exception as e:
                raise exception.ArceaeInvalidData(self, e)
        return {}

    def get_user_info(self) -> dict:
        """
        获取玩家信息
        """
        if self.has_data():
            try:
                return self.__raw_data['userinfo']
            except Exception as e:
                raise exception.ArceaeInvalidData(self, e)
        return {}

    def get_scores_list(self) -> list:
        """
        获取所有在案的游玩记录
        """
        if self.has_data():
            try:
                return deepcopy(self.__raw_data['scores'])
            except Exception as e:
                raise exception.ArceaeInvalidData(self, e)
        return []

    def get_head_icon(self) -> str:
        """
        获取头像图片的 URL 地址
        """
        if self.has_data():
            try:
                if 'character' in self.get_user_info():
                    return 'https://redive.estertion.win/arcaea/backstage/icons/' + str(
                        self.get_user_info()['character']) + '_icon.png'
                elif 'user_code' in self.get_user_info() and self.get_user_info()['user_code'] in {'000000001',
                                                                                                   '000000002'}:
                    return 'https://redive.estertion.win/arcaea/backstage/icons/' + {'000000001': '0', '000000002': '1'}[
                        self.get_user_info()['user_code']] + '_icon.png'
            except Exception as e:
                raise exception.ArceaeInvalidData(self, e)
        return ''

    def get_ptt_block(self) -> str:
        """
        获取 PTT (潜力值) 对应的数值框图片 URL 地址
        """
        try:
            ptt: int = self.get_user_info()['rating']
        except Exception as e:
            raise exception.ArceaeInvalidData(self, e)
        if ptt < 0:
            return 'https://wiki.arcaea.cn/images/3/34/Rating_off.png'
        elif ptt < 350:
            return 'https://wiki.arcaea.cn/images/2/2f/Rating_0.png'
        elif ptt < 700:
            return 'https://wiki.arcaea.cn/images/1/10/Rating_1.png'
        elif ptt < 1000:
            return 'https://wiki.arcaea.cn/images/4/44/Rating_2.png'
        elif ptt < 1100:
            return 'https://wiki.arcaea.cn/images/5/56/Rating_3.png'
        elif ptt < 1200:
            return 'https://wiki.arcaea.cn/images/9/9a/Rating_4.png'
        elif ptt < 1250:
            return 'https://wiki.arcaea.cn/images/1/1a/Rating_5.png'
        else:
            return 'https://wiki.arcaea.cn/images/e/ee/Rating_6.png'

    def get_b30(self) -> list:
        """
        获取玩家的 b30 (最好30次成绩) 记录
        """
        try:
            scores = self.get_scores_list()
            scores.sort(key=lambda x: x['rating'], reverse=True)
            return scores[:30]
        except exception.ArceaeBaseException as e:
            raise e
        except Exception as e:
            raise exception.ArceaeInvalidData(self, e)

    def get_r10(self) -> list:
        """
        获取玩家最近 30 次成绩中最好的 10 次
        """
        scores = self.get_scores_list()
        ans = {}
        try:
            scores.sort(key=lambda x: x['time_played'], reverse=True)
            while scores and len(ans) < 30:
                now = scores.pop(0)
                if now['song_id'] in ans and now['rating'] > ans[now['song_id']]['rating']:
                    ans[now['song_id']] = now
                else:
                    ans[now['song_id']] = now
            if ans:
                ans = list(ans.values())
                ans.sort(key=lambda x: x['rating'], reverse=True)
                ans = ans[:10]
                return ans
            else:
                return []
        except exception.ArceaeBaseException as e:
            raise e
        except Exception as e:
            raise exception.ArceaeInvalidData(self, e)

    def __str__(self) -> str:
        return self.__friend_code

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, ArcData) and __o.__raw_data == self.__raw_data

    def __repr__(self) -> str:
        return 'ArcData("' + self.__friend_code + '", has_data = ' + str(self.has_data()) + ') at' + str(
            id(self)) + '\n' + str(self.__raw_data)

"""
Printer 支持模块
"""

import json
import asyncio
import os
from asyncio.proactor_events import _ProactorBasePipeTransport

import aiohttp
import requests
from io import BytesIO
from pathlib import Path
from os import remove, path
from typing import Dict, Tuple, Union
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from functools import wraps

import arceae_m.data
import arceae_m.exception

ArcData = arceae_m.data.ArcData
ArceaePrinterError = arceae_m.exception.ArceaePrinterError
ArceaePrinterNetworkError = arceae_m.exception.ArceaePrinterNetworkError
ArceaeInvalidData = arceae_m.exception.ArceaeInvalidData
ArceaeBaseException = arceae_m.exception.ArceaeBaseException


class Printer:
    """
    获取并渲染图片数据
    """
    _arc_data: ArcData
    # 嵌入 ArcData 对象
    _position: Dict[str, Dict[str, int]]
    # 图片坐标字典，从 picture/position.json 中获取
    _picture_path: Path

    # picture 文件夹的路径

    def __init__(self, arc_info: Union[ArcData, str]) -> None:
        """
        传入好友码或 ArcData 对象
        """
        self._picture_path = (Path(__file__).resolve() /
                              '../picture').resolve()
        path = self._picture_path / 'position.json'
        with open(path, 'r', encoding='utf-8') as f:
            self._position = json.load(f)
        if isinstance(arc_info, str):
            arc_info = ArcData(arc_info)
        if isinstance(arc_info, ArcData):
            self._arc_data = arc_info

    def _create_b30_image(self) -> Image.Image:
        """
        创建 b30 的 Image 对象
        """
        try:
            if not self._arc_data.has_data():
                self._arc_data.catch_data()
                if not self._arc_data.has_data():
                    return Image.new('RGB', (1, 1), 'black')
            if self._arc_data.get_user_info()['rating'] < 0:
                raise ArceaeInvalidData(self, '该玩家隐藏了潜力值')
            # b30/r10 有可能不满数量
            background = Image.open(self._picture_path / 'BackgroundB30.png')
            board = ImageDraw.Draw(background)
            font_gothic_32 = ImageFont.truetype(
                str(self._picture_path / 'GOTHIC.TTF'), 32)
            font_gothic_36 = ImageFont.truetype(
                str(self._picture_path / 'GOTHIC.TTF'), 36)
            font_gothic_44 = ImageFont.truetype(
                str(self._picture_path / 'GOTHIC.TTF'), 44)
            font_gothic_48 = ImageFont.truetype(
                str(self._picture_path / 'GOTHIC.TTF'), 48)
            font_gothic_72 = ImageFont.truetype(
                str(self._picture_path / 'GOTHIC.TTF'), 72)
            font_segoeui_36 = ImageFont.truetype(
                str(self._picture_path / 'SEGOEUI.ttf'), 36)
            font_segoeui_72 = ImageFont.truetype(
                str(self._picture_path / 'SEGOEUI.ttf'), 72)
            song_dict = self._arc_data.get_songs_dict()
            score_data = self._arc_data.get_b30()

            semaphore = asyncio.Semaphore(30)
            session = aiohttp.ClientSession()

            def get_image(url: str) -> Image.Image:
                try:
                    return Image.open(BytesIO(requests.get(url).content))
                except Exception as e:
                    raise ArceaePrinterNetworkError(self, e)

            async def catch_img(url: str):
                async with semaphore:
                    try:
                        async with session.get(url) as response:
                            img = await response.read()
                            return Image.open(BytesIO(img))
                    except aiohttp.ClientError as e:
                        raise ArceaePrinterNetworkError(self, e)
                    except Exception as e:
                        raise ArceaePrinterError(self, e)

            async def print_box(number: int) -> None:
                """
                number start at 1,
                index start at 0
                """
                # print('print box ' + str(number))
                index = number - 1
                x = self._position[str(number)]['x']
                y = self._position[str(number)]['y']

                image_songs = await catch_img(
                    self._arc_data.get_song_paint(score_data[index]["song_id"]))

                str_constant_song_title = '[' + str(score_data[index]["constant"]) + ']' + \
                                          song_dict[score_data[index]["song_id"]]["title"]["en"]
                if len(str_constant_song_title) > 19:
                    str_constant_song_title = str_constant_song_title[:19] + '...'
                board.text((x + 334, y + 41), str_constant_song_title,
                           fill="black", anchor="lt", font=font_gothic_44)

                str_score = "{:,}".format(
                    score_data[index]["score"]).replace(',', "'")
                str_score = "{:0>10}".format(str_score)
                board.text((x + 334, y + 101), str_score, fill="black",
                           anchor="lt", font=font_segoeui_72)

                str_rating = "| {:.4f}".format(score_data[index]["rating"])
                board.text((x + 684, y + 124), str_rating, fill="black",
                           anchor="lt", font=font_segoeui_36)

                str_buttom = "P{0}(+{1})|F{2}|L{3}".format(score_data[index]["perfect_count"], score_data[index]
                ["shiny_perfect_count"], score_data[index]["near_count"], score_data[index]["miss_count"])
                board.text((x + 869, y + 281), str_buttom, fill="black",
                           anchor="rd", font=font_gothic_32)
                # 缩放图片
                image_songs_resized = image_songs.resize((301, 301))
                # 放置图片
                background.paste(image_songs_resized, (x, y, x + 301,
                                                       y + 301))
                # print('box ' + str(number) + 'printed')

            def print_userinfo() -> None:
                # print('print userinfo')
                user_name: str = self._arc_data.get_user_info()['name']
                user_name_position: Tuple[int, int] = (
                    self._position['user_name']['x'], self._position['user_name']['y'])
                arceae_id: str = self._arc_data.get_user_info()['user_code']
                arceae_id_position: Tuple[int, int] = (
                    self._position['arceae_id']['x'], self._position['arceae_id']['y'])
                # 👆arceae_id 直接放，没有顺序
                head_icon = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
                ptt_block = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
                try:
                    head_icon = get_image(self._arc_data.get_head_icon())
                    ptt_block = get_image(self._arc_data.get_ptt_block())
                except ArceaeBaseException:
                    ...
                except Exception as e:
                    raise e
                head_icon_position: Tuple[int, int] = (
                    self._position['head_icon']['x'], self._position['head_icon']['y'])
                # ^W225 H227
                ptt_block_position: Tuple[int, int] = (
                    self._position['ptt_block']['x'], self._position['ptt_block']['y'])
                # ^W159 H159
                ptt: str
                ptt_position: Tuple[int, int] = (
                    self._position['ptt']['x'], self._position['ptt']['y'])
                b30: str
                r10: str
                b30_r10: str
                b30_r10_position: Tuple[int, int] = (
                    self._position['b30_r10']['x'], self._position['b30_r10']['y'])
                # 这下面的是赋值用语句，不用管
                rating = self._arc_data.get_user_info()['rating']
                ptt = str(rating // 100) + '.' + str(rating % 100)
                b30_list = self._arc_data.get_b30()
                b30_num = 0.0
                for score in b30_list:
                    b30_num += score['rating']
                b30_num /= 30
                b30 = str(round(b30_num * 1000) / 1000)
                r10_list = self._arc_data.get_r10()
                r10_num = 0.0
                for score in r10_list:
                    r10_num += score['rating']
                r10_num /= 10
                r10 = str(round(r10_num * 1000) / 1000)
                b30_r10 = 'Total Best 30: ' + b30 + '         Recent Best 10: ' + r10

                # Color:#f9f9f9

                def text_with_shadow(pos: Tuple[int, int], text: str,
                                     fill: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]], font) -> None:
                    # TODO(@IMurKuroMI): 完成文本阴影
                    up = Image.new('RGBA', (2000, 200), (0, 0, 0, 0))
                    up_draw = ImageDraw.Draw(up)
                    up_draw.text((1000, 140), text, fill, font, 'ms')
                    down = Image.new('RGBA', (2000, 200), (0, 0, 0, 0))
                    down_draw = ImageDraw.Draw(down)
                    down_draw.text((1000, 140), text, (0, 0, 0, 60),
                                   font, 'ms', stroke_width=8)
                    down = down.filter(ImageFilter.GaussianBlur(20))
                    down.paste(up, (0, 0), mask=up.split()[3])
                    background.paste(down, (0, pos[1] - 140), mask=down.split()[3])

                # TODO(@Bessky): 放置以上内容，顺序 head_icon -> ptt_block -> ptt
                head_icon = head_icon.resize((225, 227))
                background.paste(
                    head_icon, (
                        head_icon_position[0], head_icon_position[1], head_icon_position[0] + 225,
                        head_icon_position[1] + 227),
                    mask=head_icon.split()[3])
                ptt_block = ptt_block.resize((159, 159))
                background.paste(
                    ptt_block, (
                        ptt_block_position[0], ptt_block_position[1], ptt_block_position[0] + 159,
                        ptt_block_position[1] + 159),
                    mask=ptt_block.split()[3])
                # text_with_shadow(ptt_position, ptt, fill="white",
                #                  font=font_GOTHIC_36)
                text_with_shadow(user_name_position, user_name,
                                 fill="white", font=font_gothic_72)
                text_with_shadow(b30_r10_position, b30_r10,
                                 fill="white", font=font_gothic_72)
                board.text(ptt_position, ptt, (0, 0, 0),
                           font=font_gothic_44, anchor='ms', stroke_width=1)
                board.text(ptt_position, ptt, (255, 255, 255),
                           font=font_gothic_44, anchor='ms')
                board.text(arceae_id_position, arceae_id,
                           (255, 255, 255), font=font_gothic_36, anchor='ls')
                # print('userinfo printed')

            b30_len = len(score_data)
            if b30_len > 0:
                if os.name == 'nt':
                    # 在 Windows 系统下解决 asyncio 对 aiohttp 的支持问题
                    def silence_event_loop_closed(func):
                        @wraps(func)
                        def wrapper(self, *args, **kwargs):
                            try:
                                return func(self, *args, **kwargs)
                            except RuntimeError as e:
                                if str(e) != 'Event loop is closed':
                                    raise

                        return wrapper

                    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)

                async def run():
                    tasks = [asyncio.ensure_future(
                        print_box(i + 1)) for i in range(b30_len)]
                    await asyncio.wait(tasks)
                    await session.close()

                asyncio.get_event_loop().run_until_complete(run())
            print_userinfo()
            return background
        except ArceaePrinterNetworkError as e:
            raise e
        except Exception as e:
            raise ArceaePrinterError(self, e)

    def get_filename(self) -> str:
        """
        获取该 ArcData 对象对应的图片文件名
        """
        try:
            return self._arc_data.get_user_info()['user_code'] + '.png'
        except ArceaeBaseException as e:
            raise e
        except Exception as e:
            raise ArceaeInvalidData(self, e)

    def build_picture(self) -> str:
        """
        在工作路径创建图片文件 (b30) ，返回文件名

        在使用完图片后调用 `remove_picture` 销毁
        """
        file_name = ''
        built_image = self._create_b30_image()
        file_name = self.get_filename()
        built_image.save(file_name)
        return path.abspath(file_name)

    def remove_picture(self) -> None:
        """
        销毁内嵌 ArcData 对象对应的图片文件
        """
        try:
            if path.exists(self.get_filename()):
                remove(self.get_filename())
        except ArceaeBaseException as e:
            raise e
        except Exception as e:
            raise ArceaePrinterError(self, e)

    def __del__(self) -> None:
        self.remove_picture()

    def __str__(self) -> str:
        return str(self._arc_data)

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Printer) and __o._arc_data == self._arc_data

    def __repr__(self) -> str:
        return 'Printer("' + str(self._arc_data) + '") at ' + str(id(self)) + '\n' + str(
            self._arc_data.get_user_info()) + '\n' + str(self._arc_data.get_b30()) + '\n' + str(
            self._arc_data.get_r10())

    @property
    def arc_data(self):
        return self._arc_data

"""
paint_catch 模块，提供一系列用于支持从 Arceae Wiki 获取曲绘 URL 地址的方法

* `save_song_pic_dict`: 保存曲目对曲绘 URL 路径字典到 json 文件中
* `load_song_pic_dict`: 读取曲目对曲绘 URL 路径字典并返回
* `get_song_pic_url`: 获取曲绘 URL 地址，自动协调缓存与json文件的数据
* `updata_song_pic_dict_file`: 按传入的曲目字典更新缓存的字典与存储的json文件，返回执行结果
"""

import os
import json
from typing import Dict
from bs4 import BeautifulSoup
import urllib.request as urlreq
import arceae_m.exception
ArceaeSongPaintModuleError = arceae_m.exception.ArceaeSongPaintModuleError
"真实屎山（不"

_song_paint_url_dict: Dict[str, str] = {}
_song_paint_file_time = 0.0
_song_paint_file_name = 'song_paint_URLs.json'


def catch_url(file_name: str) -> str:
    try:
        url = 'https://wiki.arcaea.cn/index.php/File:' + file_name
        request = urlreq.urlopen(url)
        obj = BeautifulSoup(request.read(), 'lxml')
        img = obj.select('#file > a > img')[0]
        return 'https://wiki.arcaea.cn' + img.attrs['src']
    except Exception as e:
        raise ArceaeSongPaintModuleError(e)


def catch_song_pic_url(song_id: str) -> str:
    return catch_url('Songs_' + song_id + '.jpg')


def catch_song_pic_dict(songs_dict: dict) -> dict:
    try:
        ans = {}
        for id in songs_dict:
            url = catch_song_pic_url(id)
            if url:
                ans[id] = url
        return ans
    except Exception as e:
        raise ArceaeSongPaintModuleError(e)


def save_song_pic_dict(url_dict: dict = _song_paint_url_dict) -> None:
    """
    保存曲目对曲绘 URL 路径字典到 json 文件中

    * `url_dict`: 要保存的曲目对曲绘 URL 路径字典，默认值为模块内置缓存字典，建议不更改
    """
    global _song_paint_file_time
    try:
        with open(_song_paint_file_name, 'w', encoding='utf-8') as f:
            json.dump(url_dict, f, ensure_ascii=False, indent=2)
        _song_paint_file_time = os.path.getmtime(_song_paint_file_name)
    except Exception as e:
        raise ArceaeSongPaintModuleError(e)


def load_song_pic_dict() -> dict:
    """
    读取曲目对曲绘 URL 路径字典并返回

    会同时替换模块对应的缓存字典
    """
    global _song_paint_url_dict, _song_paint_file_time
    try:
        with open(_song_paint_file_name, 'r', encoding='utf-8') as f:
            _song_paint_url_dict = json.load(f)
        _song_paint_file_time = os.path.getmtime(_song_paint_file_name)
        return _song_paint_url_dict
    except json.JSONDecodeError as e:
        os.rename(_song_paint_file_name, _song_paint_file_name + '.err_bak')
        save_song_pic_dict(_song_paint_url_dict)
        raise ArceaeSongPaintModuleError(e)
    except Exception as e:
        save_song_pic_dict(_song_paint_url_dict)
        raise ArceaeSongPaintModuleError(e)
    finally:
        return {}


def get_song_pic_url(song_id: str) -> str:
    """
    获取曲绘 URL 地址，自动处理缓存与json文件

    本模块的核心方法

    * `song_id`: 曲目id，为英文字符组成的字符串
    """
    global _song_paint_file_time, _song_paint_url_dict
    try:
        if not os.path.isfile(_song_paint_file_name):
            save_song_pic_dict(_song_paint_url_dict)
        m_time = os.path.getmtime(_song_paint_file_name)
        if m_time > _song_paint_file_time:
            _song_paint_url_dict = load_song_pic_dict()
        if song_id in _song_paint_url_dict:
            return _song_paint_url_dict[song_id]
        else:
            url = catch_song_pic_url(song_id)
            if url:
                _song_paint_url_dict[song_id] = url
                save_song_pic_dict(_song_paint_url_dict)
            return url
    except:
        return catch_song_pic_url(song_id)


def update_song_pic_dict_file(songs_dict: dict) -> bool:
    """
    按传入的曲目字典更新缓存的字典与存储的json文件，返回执行结果

    * `songs_dict`: 曲目字典
    """
    try:
        global _song_paint_url_dict
        _song_paint_url_dict = catch_song_pic_dict(songs_dict)
        save_song_pic_dict(_song_paint_url_dict)
        return True
    except Exception as e:
        raise ArceaeSongPaintModuleError(e)
    finally:
        return False

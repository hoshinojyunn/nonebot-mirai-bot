"""
Arceae 玩家数据获取模块
支持从第三方后端服务器获取包括 B30 在内的玩家数据和图片渲染
由于 616 的限制，使用的数据获取方法非常慢，建议使用 Application 类来完成异步获取数据

* `ArcData`: 用户查询数据封装类
* `Printer`: b30 图片生成类，会内嵌 ArcData 对象
* `Application`: 多线程异步查询应用类，采用回调函数，会内嵌 Printer 对象
* `paint_catch`: 曲绘获取模块
"""

# "requirements.txt" 文件中存储的是依赖包，可以使用 "pip install -r requirements.txt" 安装

from arceae_m.application import Application
from arceae_m.printer import Printer
from arceae_m.data import ArcData
from arceae_m import paint_catch

__author__ = [
    "IMurKuroMI (IMurKuroMI@outlook.com)",
    "Bessky (bessky-@outlook.com)"
]
__version__ = "0.02.0"

__all__ = ['ArcData', 'Printer', 'paint_catch', 'Application']

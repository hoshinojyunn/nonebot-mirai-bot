import threading
import asyncio
from typing import Union
import arceae_m.data
import arceae_m.printer

from .exception import *
ArcData = arceae_m.data.ArcData
Printer = arceae_m.printer.Printer


class Application(threading.Thread):
    """
    应用类，提供回调接口，多线程执行

    目前仅设计用于获取b30图片

    运行结束之后可以访问 Printer 类型成员对象 _printer 进行额外的操作（不推荐）
    """

    def __init__(self,
                 arceae_id: Union[str, ArcData, Printer],
                 on_start=None,
                 on_receive=None,
                 on_error=None,
                 on_stop=None):
        """
        * arceae_id: 要嵌入的 Arceae 玩家数据，最后会被初始化为 Printer 对象
        * on_start(app: Application): 启动线程时调用的回调函数，参数 1 为该对象
        * on_receive(app: Application): 请求在远端服务器完成排队后，开始接收数据时调用的回调函数，此后开始接收成绩数据， 参数 1 同上
        * on_error(app: Application, e: ArceaeBaseException): 产生错误时调用的回调函数，参数 1 同上，参数 2 为抛出的错误对象
        * on_stop(app: Application, result_dict: list): 结束连接时调用的回调函数，无论是否产生错误最后都会被调用，
        `执行结束后会删除产生的图片`

        参数 1 同上，

        参数 2 为查询结果字典，若获取失败则为空；关键字有：

            'b30_path': b30图片路径，注意在该回调函数执行结束后会被删除

            'ArcData': ArcData对象
        """
        super(Application, self).__init__(name='ArceaeCatcherThread( "' + str(arceae_id) + '" )', daemon=True)
        if isinstance(arceae_id, str) or isinstance(arceae_id, ArcData):
            self._printer = Printer(arceae_id)
        elif isinstance(arceae_id, Printer):
            self._printer = arceae_id
        self.on_start = on_start
        self.on_receive = on_receive
        self.on_error = on_error
        self.on_stop = on_stop
        self.stop_flag = False

    def run(self) -> None:
        path = ''
        try:
            if callable(self.on_start):
                self.on_start(self)
            if callable(self.on_receive):
                def received():
                    self.on_receive(self)

                self._printer.arc_data.catch_data(received)
            else:
                self._printer.arc_data.catch_data()
            asyncio.set_event_loop(asyncio.new_event_loop())
            path = self._printer.build_picture()
        except ArceaeBaseException as e:
            if callable(self.on_error):
                self.on_error(self, e)
        finally:
            if callable(self.on_stop):
                result = {
                    'b30_path': path,
                    'ArcData': self._printer.arc_data
                }
                self.on_stop(self, result)
            try:
                self._printer.remove_picture()
            except Exception as e:
                print(repr(e))
            finally:
                self.stop_flag = True

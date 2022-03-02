"""
异常类
"""
__all__ = [
    'ArceaeBaseException',
    'ArceaeQueryFailed',
    'ArceaeInvalidData',
    'ArceaeSongPaintModuleError',
    'ArceaePrinterError',
    'ArceaePrinterNetworkError'
]

from typing import Union, Any


class ArceaeBaseException(Exception):
    """
    异常类基类
    """

    def __init__(self, arceae_info: Union[str, Any], error_info: Union[Exception, str]):
        """
        arceae_info 可以是字符串，或是 Printer, ArcData 对象
        建议使用 isinstance 函数进行判断
        """
        self.arceae_info = repr(arceae_info)
        self.error_info = error_info

    def __str__(self):
        return str(self.error_info)


class ArceaeQueryFailed(ArceaeBaseException):
    """
    数据获取请求失败
    """


class ArceaeInvalidData(ArceaeBaseException):
    """
    访问的数据非法
    """


class ArceaeSongPaintModuleError(ArceaeBaseException):
    """
    曲绘获取模块错误
    """

    def __init__(self, error_info: Union[Exception, str]):
        super(ArceaeSongPaintModuleError, self).__init__('', error_info)


class ArceaePrinterError(ArceaeBaseException):
    """
    图片生成错误
    """


class ArceaePrinterNetworkError(ArceaePrinterError):
    """
    图片生成时产生的网络错误
    """

#!/usr/bin/env python
# coding=utf-8


class RCException(Exception):
    '''base exception'''
    error_code = 10000
    __name__ = '自定义异常'
    ding_receiver = []
    ding_robot = []

    def __init__(self, *args, ding_receiver=None, ding_robot=None, **kwargs):
        self.ding_receiver = ding_receiver
        self.ding_robot = ding_robot
        Exception.__init__(self, *args, **kwargs)


class RCParaValiException(RCException):
    error_code = 10001
    __name__ = '参数异常'


class RCRespValiException(RCException):
    error_code = 10002
    __name__ = '接口返回校验异常'


class RCReqErrorException(RCException):
    error_code = 10011
    __name__ = '请求时异常'


class RCStorageException(RCException):
    error_code = 10012
    __name__ = '操作存储时异常'


class RCBusiException(RCException):
    error_code = 10013
    __name__ = '业务服务异常'


class RCOPException(RCException):
    error_code = 10020
    __name__ = '某种操作时异常'



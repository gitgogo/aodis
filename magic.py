#!/usr/bin/env python
import datetime
from flask import Response
from werkzeug.datastructures import Headers
from simplejson.errors import JSONDecodeError as SimpleJSONDecodeError
from json import JSONDecodeError

from flask import current_app
from flask.json import jsonify
from flask import request
# from werkzeug.contrib.cache import SimpleCache
import requests
from requests.exceptions import HTTPError, BaseHTTPError, ConnectTimeout, ConnectionError, Timeout

from ex import RCParaValiException, RCRespValiException, RCReqErrorException


class ValidateParams:
    def __init__(self, app):
        self.app = app

    def rc_vp(self, *required_args):
        if request.method == 'GET':
            missed = [k for k in required_args if k not in request.args]
        else:
            missed = [k for k in required_args if k not in request.json]

        if missed:
            raise RCParaValiException('缺少参数: {}'.format(', '.join(missed)))


class CommonRequest(object):
    """
    发送HTTP请求，并对指定项进行校验。目前只支持json
    """

    def __init__(self, app=None):
        self.app = app

    def rc_req(self, method=None, url=None, validate=None, **kwargs):
        app = self.app or current_app
        # 校验必填项是否存在
        if not method:
            raise RCParaValiException("调用rc_req时缺少参数method")
        if not url:
            raise RCParaValiException("调用rc_req时缺少参数url")
        # 获取请求各项
        app.logger.info(("开始发送请求:\n"
                         "url: {}\n"
                         "method: {}\n"
                         "{}").format(url, method,
                                      "\n".join(['{}: {}'.format(k, str(v)) for (k, v) in kwargs.items()])))
        try:
            # 发送请求
            resp = requests.request(method=method, url=url, **kwargs)
            app.logger.info("请求响应码为: %s" % resp.status_code)
            app.logger.info("请求响应为: %s" % resp.content)
            # 判断请求返回是否为非200
            if resp.status_code not in (200, 201, 202):
                app.logger.error("请求返回非200响应码")
                raise RCRespValiException("请求返回非200响应码")

            try:
                resp_content = resp.json()
                is_resp_json = True
            except (SimpleJSONDecodeError, JSONDecodeError, TypeError):
                is_resp_json = False
                resp_content = resp.content

            if validate:
                if not is_resp_json:
                    raise RCRespValiException("请求返回的不是json格式")
                # 校验请求响应的校验项是否正确
                for key, value in validate.items():
                    tmp = resp_content
                    key_list = key.split('.')
                    for each in key_list:
                        # 判断key是否存在
                        if each not in tmp.keys():
                            app.logger.error("校验key值错误，不存在key值: %s，响应为: %s" % (key, resp_content))
                            raise RCRespValiException(
                                "校验key值错误，不存在key值: %s，响应为: %s" % (key, resp_content))
                        else:
                            tmp = tmp.get(each)
                    # 判断key对应的value是否为预期值
                    if tmp != value:
                        app.logger.error("HTTP请求校验失败，%s的预期值为: %s，实际值为: %s，响应为: %s " %
                                         (key, str(value), str(tmp), resp_content))
                        raise RCRespValiException("HTTP请求校验失败，%s的预期值为: %s，实际值为: %s，响应为: %s" %
                                                  (key, str(value), tmp, resp_content))
            return resp_content
        except (HTTPError, BaseHTTPError, ConnectTimeout, ConnectionError, Timeout) as ex:
            # 处理requests抛出的异常
            app.logger.error("请求有异常抛出: %s" % str(ex))
            raise RCReqErrorException("请求有异常抛出: %s" % str(ex))


class CommonResponse:
    """
    返回HTTP请求
    """

    def __init__(self, app=None):
        self.app = app

    def ok(self, data='', msg='success'):
        return self.__json(code=0, msg=msg, data=data)

    def error(self, code, msg, data=''):
        return self.__json(code=code, msg=msg, data=data)

    def not_found(self, title='后端接口未找到', msg=None):
        return self.__json(code=404, title=title, message=msg),404

    def __json(self, **kwargs):
        return jsonify(**kwargs)


def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,token'
    return response

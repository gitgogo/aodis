# -* - coding: UTF-8 -* -
import requests
import importlib
import sys
import traceback
import json as _json

stdout = sys.stdout
stderr = sys.stderr
stdin = sys.stdin
importlib.reload(sys)

sys.stdout = stdout
sys.stderr = stderr
sys.stin = stdin

out_time = 60


class HttpClient:
    """docstring for HttpClient"""
    def __init__(self, cookie=False):
        self.cookie = cookie

    @staticmethod
    def get_session():
        return requests.session()

    @staticmethod
    def get_request(url, para=None, header=None, cookie=None, session=None, verify=False, proxies=None):
        if session:
            response = session.get(url, params=para, headers=header,
                                   cookies=cookie, timeout=out_time, verify=verify, proxies=proxies)
        else:
            response = requests.get(url, params=para, headers=header,
                                    cookies=cookie, timeout=out_time, verify=verify, proxies=proxies)
        return response

    @staticmethod
    def post_request(url, para=None, header=None, json=None, data=None, cookie=None, session=None, verify=False, proxies=None):
        if session:
            response = session.post(url, json=json, data=data, params=para, headers=header,
                                    cookies=cookie, timeout=out_time, verify=verify, proxies=proxies)
        else:
            response = requests.post(url, json=json, data=data, params=para, headers=header,
                                     cookies=cookie, timeout=out_time, verify=verify, proxies=proxies)
        return response

    @staticmethod
    def api_request(url, para=None, u_method="GET", header=None, json=None, data=None,
                    cookie=None, session=None, print_data_flag=True, verify=False, proxies=None):
        """处理请求，返回原始json串"""
        if print_data_flag:
            print("地址：", url, u_method)
            if header:
                print("header参数：", str(header).replace("'", '"'))
            if data:
                print("post data参数：", str(data).replace("'", '"'))
            if json:
                print("post json参数：", str(json).replace("'", '"'))
            if para:
                print("path参数：", str(para).replace("'", '"'))

        try:
            ret = ""
            if u_method.lower() == 'get':
                ret = HttpClient.get_request(url, para, header, cookie, session, verify, proxies=proxies)
            elif u_method.lower() == 'post':
                ret = HttpClient.post_request(url, para, header, json, data, cookie, session, verify, proxies=proxies)

            if print_data_flag:
                try:
                    res_j = _json.loads(ret.text)
                    print("返回结果：", res_j)
                except Exception as e:
                    print(e)
                    print("返回结果：", ret.text[:20000])
                else:
                    print("")
            return ret
        except Exception as e:
            print(traceback.format_exc())
            raise Exception(str(e))

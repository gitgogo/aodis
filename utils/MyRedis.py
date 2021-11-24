# -* - coding: UTF-8 -* -
import traceback
import redis


class McyRedisSingle(object):
    redis_conn = None

    def __init__(self, host, port, password=None):
        if McyRedisSingle.redis_conn is None:
            self.host = host
            self.port = port
            self.password = password
            self.get_connector()

    def get_connector(self):
        redis_conn = None
        try:
            if self.password:
                redis_conn = redis.StrictRedis(connection_pool=redis.ConnectionPool(
                    host=self.host, port=self.port, password=self.password, decode_responses=True))
            else:
                redis_conn = redis.StrictRedis(connection_pool=redis.ConnectionPool(
                    host=self.host, port=self.port))
            if not redis_conn:
                print("连接redis单机失败")
        except Exception as e:
            print(traceback.format_exc())
            print("连接redis单机失败", e)
        finally:
            McyRedisSingle.redis_conn = redis_conn


def get_redis(host="cccc", port=6379, pwd='mmmmm'):
    con = McyRedisSingle(host, port, pwd)
    return con.redis_conn


def set_v(key, value):
    con = get_redis()
    print("保存redis数据: " + str(key) + ": " + str(value))
    res = con.set(key, value) if con else False
    print("保存redis数据结果" + str(res))
    return res


def setex_v(key, tim, value):
    con = get_redis()
    print("保存redis数据: " + str(key) + ": " + str(value))
    res = con.setex(key, tim, value) if con else False
    print("保存redis数据结果" + str(res))
    return res


def get_v(key):
    print("获取redis key: ", key)
    con = get_redis()
    res = con.get(key)
    res_str = str(res) if res else ""
    print("获取redis数据: ", res_str)
    return res_str


if __name__ == '__main__':
    # set_v('mcy_crs_id', "01fc36e784898539250de8a001b905069bysfyym")
    # set_v('mcy_crs_id', "")
    get_v('vvvv')
    get_v('bbbbbbb')

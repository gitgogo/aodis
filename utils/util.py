import re
import datetime
import math
import time
import random


def get_num(some):
    pattern = re.compile(r'\d+')
    return pattern.search(some).group()


def date_utc_cst(utc_date):
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    utcTime = datetime.datetime.strptime(utc_date, UTC_FORMAT)
    localtime = utcTime + datetime.timedelta(hours=8)
    return str(localtime)


def get_db_info(ori_str):
    stu_id = int(ori_str)
    temp_a = stu_id % 10000 % 1024
    db_no = math.floor(temp_a / 256)
    order_info_no = math.floor((temp_a % 256) / 64)
    order_detail_no = math.floor((temp_a % 256) / 8)
    res_list = [db_no, order_info_no, order_detail_no]
    print(res_list)
    return res_list


def get_random_int_to_str(length: int):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def get_time_strap():
    t = time.time()
    return str(int(round(t * 1000)))


def get_time_format(del_days=0, del_min=0):
    time_array = time.localtime()
    t_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    s_time = datetime.datetime.strptime(t_time, '%Y-%m-%d %H:%M:%S')
    day_del = datetime.timedelta(days=del_days, minutes=del_min)
    return str((s_time + day_del))


if __name__ == '__main__':
    utc_date = "2020-12-02T09:12:46.000Z"
    print(date_utc_cst(utc_date))

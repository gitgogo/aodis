from utils.mysqldb import MysqlClient
from datetime import datetime

db = MysqlClient()


def list_api(page=1, limit=10, name=''):
    where = "where 1=1"
    if name:
        where += " and name=" + repr(name)

    sql = 'SELECT sql_calc_found_rows id, name, creator, create_time,' \
          ' update_time  FROM fuzz.interface_info {0} ORDER BY ID DESC limit {1},{2}'.format(where,
                                                                                             page * limit,
                                                                                             limit)

    get_total_sql = "SELECT FOUND_ROWS() as total;"

    result = db.select([sql, get_total_sql])
    for one in result[0]:
        print("one", one)
        one['update_time'] = one.get('update_time').strftime("%Y-%m-%d %H:%M:%S") if one.get('update_time') else ""
        one['create_time'] = one.get('create_time').strftime("%Y-%m-%d %H:%M:%S") if one.get('create_time') else ""
    print("result : ", result)
    return {'list': result[0], 'total': result[1][0]['total']}


def insert_api(data={}):
    res = {}
    if data:
        daily_date = str(datetime.date(datetime.now()))
        name = data['name']
        busi_line = data['busi_line']
        item_type = data['item_type']
        priority = data['priority']
        progress = data['progress']
        period = data['period']
        manpower = data['manpower']
        sql = "insert into daily(daily_date, name, busi_line, item_type, priority, progress, period, manpower, " \
              "create_time, update_time) value({0},{1},{2},{3},{4},{5},{6},{7},NOW(),NOW());". \
            format(repr(daily_date), repr(name), repr(busi_line), repr(item_type), repr(priority), repr(progress),
                   repr(period), repr(manpower))
        db.operate(sql)
        return res
    else:
        print('传参缺失')
        return {'msg': '数据添加失败'}

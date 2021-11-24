import pymysql


class MysqlClient:
    def __init__(self, user='root', passwd='',  host='localhost', charset='utf8'):
        self.con = pymysql.connect(host=host,
                                   user=user,
                                   password=passwd,
                                   port=3306,
                                   db='aodsi',
                                   charset=charset)
        # 游标设置为字典类型
        self.cur = self.con.cursor(cursor=pymysql.cursors.DictCursor)
        # self.cur = self.con.cursor()

    def operate(self, sql, val=None):
        result = -1
        try:
            result = self.cur.execute(sql, val)
            result = self.cur.fetchall()
            # new_id = self.cur.lastrowid
        except Exception as e:
            print(e)
        self.con.commit()
        self.close()
        return result

    def select(self, sql, val=None):
        result = ''
        try:
            self.cur.execute(sql, val)
            result = self.cur.fetchall()
        except Exception as e:
            print(e)
        self.close()
        return result

    def close(self):
        self.cur.close()
        self.con.close()


if __name__ == '__main__':
    db = MysqlClient()
    id = 6
    sql = "xxxxx"
    sql1 = "select * from "
    data = db.operate(sql1)
    print(data)

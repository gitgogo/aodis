from flask import current_app as app, request
from flask import Blueprint
import datetime
from service.daily_service import *

daily = Blueprint('daily', __name__, url_prefix='/api/daily')


@daily.route('/list', methods=['GET'])
def get_list():
    page = request.args.get('page')
    limit = request.args.get('limit')
    page = page if page else 1
    limit = limit if limit else 10
    data = list_api(page, limit)
    data = [
        {
            "id": 1,
            "date": "2021-10-02",
            "busi_line": "商业化",
            "status": "完成",
            "author": "tony",
            "create_time": "2021-10-20 11:11:00"
        },
        {
            "id": 2,
            "date": "2021-10-04",
            "busi_line": "分享裂变",
            "status": "未完成",
            "author": "lily",
            "create_time": "2021-10-20 12:11:00"
        },
        {
            "id": 3,
            "date": "2021-10-07",
            "busi_line": "用户体验",
            "status": "开始",
            "author": "jack",
            "create_time": "2021-10-20 10:11:00"
        }
    ]
    return app.rc_resp.ok(data=data)


@daily.route('/add', methods=['POST'])
def insert():
    params = request.json
    data = insert_api(data=params)
    return app.rc_resp.ok(data=data)

#!/usr/bin/env python
import logging
import os
from logging.handlers import RotatingFileHandler
from collections import defaultdict
import importlib
from flask import Flask
from ext import db
from config import config
from magic import CommonRequest, CommonResponse, ValidateParams, after_request
from view.daily_view import daily


def init_log(app):
    # init log
    formatter = logging.Formatter(app.config['LOG_FORMAT'])

    file_handler = RotatingFileHandler(
        app.config['LOG_PATH'],
        maxBytes=app.config['LOG_FILE_MAX_LENGTH'],
        backupCount=app.config['LOG_FILE_ROTATING_NUMBER'],
        encoding="utf8"
    )
    file_handler.setLevel(app.config['LOG_LEVEL'])
    file_handler.setFormatter(formatter)
    app.logger.setLevel('DEBUG')
    app.logger.addHandler(file_handler)


def create_app(config_name='development'):
    app = Flask(__name__)

    # 自定义返回类，跨域控制【本地调试放开】
    #app.after_request(after_request)

    # init globe_config
    config.get(config_name, config.get(os.getenv('FLASK_ENV', 'default'))).init_app(app)
    # create log/session folder
    # for dp in (os.path.dirname(app.config.get('LOG_PATH')), app.config.get('SESSION_FILE_DIR')):
    #     if not os.path.exists(dp):
    #         os.mkdir(dp)

    # init log
    init_log(app)

    # init ding msg saver
    app.ding_map = defaultdict(dict)

    # handle exception
    # app.errorhandler(404)(error404_handler(app))
    # app.errorhandler(500)(error500_handler(app))

    # register 3rd-party components
    # CAS(app=app, url_prefix='/flash/api/cas')

    # 初始化db
    db.init_app(app)

    # register magic components
    app.rc_req = CommonRequest(app).rc_req
    app.rc_resp = CommonResponse(app)
    app.rc_vp = ValidateParams(app).rc_vp

    # register business blueprint
    # for m in (''):
    #     bp_m = importlib.import_module(m).bp_master
    #     bp_d = importlib.import_module(m).bp_dev
    #     app.register_blueprint(bp_m)
    #     app.register_blueprint(bp_d)
    app.register_blueprint(daily)
    return app

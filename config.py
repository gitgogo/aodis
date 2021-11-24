
import logging
import os


class DefaultConfig:
    # log setting
    LOG_LEVEL = logging.INFO
    LOG_FILE_MAX_LENGTH = 1024 * 1024 * 1
    LOG_FILE_ROTATING_NUMBER = 10
    LOG_PATH = None
    LOG_FORMAT = '[%(asctime)s|%(filename)s:%(lineno)d:%(funcName)s|%(levelname)s]\n%(message)s '

    # session
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = 'secret_key_sdlkfhasfg813t8gfjasg81'
    SESSION_FILE_DIR = None
    SESSION_FILE_THRESHOLD = 500
    SESSION_PERMANENT = True

    # cas
    CAS_SERVER = 'http://xxx/cas/'

    # swagger setting
    SWAGGER_CONF = {
        "headers": [
        ],
        "specs": [
            {
                "endpoint": 'xx',
                "route": '/xx/api/xx_swagger.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/xx/api/xxgger_static",
        "swagger_ui": True,
        "specs_route": "/xx/api/apidocs/"
    }

    @classmethod
    def init_app(cls, app):
        app.config.from_object(cls)


class Development(DefaultConfig):
    DEV_MODE = True
    LOG_LEVEL = logging.DEBUG
    LOG_PATH = os.path.join(os.path.join(os.path.dirname(__file__), 'log'), 'log.log')
    SESSION_FILE_DIR = os.path.join(os.path.dirname(__file__), 'session')

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://work:123456@1127.0.0.1:3306/xxdev?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    # 多数据源
    SQLALCHEMY_BINDS = {
        'auth': 'mysql+pymysql://root:123456@127.0.0.1:3306/auth?charset=utf8'
    }


class Production(DefaultConfig):
    LOG_PATH = '/var/qa_tool/log/xx/xx_app.log'
    SESSION_FILE_DIR = '/var/qa_tool/session/xx'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://work:123456@localhost:3306/xx?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_RECYCLE = 290
    SQLALCHEMY_POOL_TIMEOUT = 300
    # 多数据源
    SQLALCHEMY_BINDS = {
        'auth': 'mysql+pymysql://work:123456@127.0.0.1:3306/course?charset=utf8'
    }
    # 定时任务相关配置
    JOBS = [
        # 每晚两点执行更新cookie
        {
            'id': 'update_cookie',
            'func': 'task.update_cookie:update_cookie',  # 路径：job函数名
            'args': None,
            'trigger': 'cron',
            'hour': 2
        }
    ]
    SCHEDULER_API_ENABLED = True


config = {
    'development': Development,
    'production': Production,
    'default': DefaultConfig
}

from flask import Flask
from .exts import init_exts
import config
from .urls import *
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


class My_Filter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return True


#  1.创建app
def create_app():
    """
    用于初始化
    """
    app.config.from_object(config)
    init_exts(app)
    init_logfile()
    return app


#  2.注册蓝图
def init_logfile():
    logging.basicConfig(level=logging.WARNING)
    handler = RotatingFileHandler(filename="logs/log", maxBytes=1024 * 1024 * 10, backupCount=10, encoding="utf-8")
    my_format = logging.Formatter("%(levelname)s %(filename)s:%(lineno)d %(message)s")
    handler.setFormatter(my_format)
    filter = My_Filter()
    handler.addFilter(filter)
    logger = logging.getLogger()
    logger.handlers.append(handler)

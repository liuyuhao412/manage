import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    # 数据库配置
    # SQLAlchemy和数据库的配置
    USERNAME = os.getenv("DB_USERNAME")
    PASSWORD = os.getenv("DB_PASSWORD")
    HOST = os.getenv("DB_HOST")
    PORT = os.getenv("DB_PORT")
    DATABASE = os.getenv("DB_NAME")
    DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(
        USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 动态追踪修改设置，没有设置会有警告
    SQLALCHEMY_ECHO = False  # 查询时显示原始SQL语句

    # 秘钥配置
    SECRET_KEY = os.getenv("SECRET_KEY") or "flask:manage:server:123123123"
    DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD") or "Xxx@123456"

    # 后端配置
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")  # 从环境变量读取 HOST
    PORT = int(os.getenv("FLASK_PORT", 5000))  # 从环境变量读取 PORT
    DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"  # 从环境变量读取 DEBUG

    # 邮件配置
    MAIL_SERVER = os.getenv("MAIL_SERVER")  # 邮件服务器
    MAIL_PORT = int(os.getenv("MAIL_PORT"))  # 邮件端口
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS").lower() == "true"  # 是否使用TLS
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL").lower() == "true"  # 是否使用SSL
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")  # 邮箱用户名
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # 邮箱密码
    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER", "noreply@example.com"
    )  # 默认发件人

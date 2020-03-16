#次py文件是用来集中化管理 配置
import os
config_path = os.path.abspath(os.path.dirname(__file__ ))#获取当前文件的绝对目录，为了将建立的db库放入相应的位置

class Config:
    # SQLALCHEMY_DATABASE_URI ="sqlite:///" + os.path.join(config_path,'twittor.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","sqlite:///" + os.path.join(config_path, 'twittor.db'))#与上一行不同是可以方便更改db所在的url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'abc123'
    TWEET_PER_PAGE = 5

    # MAIL_DEFAULT_SENDER = 'noreply@twittor.com'
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = 1
    # MAIL_USERNAME = 'twittoradm'
    # MAIL_PASSWORD = 'youguess'

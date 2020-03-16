from flask import Flask
from flask_sqlalchemy import SQLAlchemy #SQLAlchemy 是数据库做ORM(对象关系映射)的一个工具1.用来实现表的建立，2.还可以用来屏蔽数据库底层，使代码与底层数据库的选择无关
#SQLAlchemy是Python编程语言下的一款ORM框架，该框架建立在数据库API之上，使用关系对象映射进行数据库操作，简言之便是：将对象转换成SQL，然后使用数据API执行SQL并获取执行结果。
from flask_migrate import Migrate #Migrate用来将代码中建的数据库迁移到实际的数据库，
from twittor.config import Config
from flask_login import LoginManager

db = SQLAlchemy()#初始化
migrate = Migrate()#初始化
login_manager =LoginManager()
login_manager.login_view = 'login'

from twittor.route import index,login,logout,register,user,page_not_found,edit_profile,explore#,reset_password_request
def create_app():
   app = Flask(__name__)
   app.config.from_object(Config)
   #app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:twittor.db"#这一步也属于db，也就是SQLAlchemy的初始化
   #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #用来消除一个警告
   db.init_app(app)#将db传入flask的app，但是db初始化仍未完成，还要设置 app.config['SQLALCHEMY_DATABASE_URI']，所以上面会有赋值，从而建立sqlite数据库
   migrate.init_app(app,db)#将migrate传入flask的app
   login_manager.init_app(app)

   app.add_url_rule('/index','index', methods= ['GET','POST'])
   app.add_url_rule('/', 'index', index,methods= ['GET','POST'])
   app.add_url_rule ('/login','login',login,methods= ['GET','POST'])
   app.add_url_rule ('/logout','logout',logout)
   app.add_url_rule('/register', 'register', register,methods= ['GET','POST'])
   app.add_url_rule ('/<username>','profile',user,methods= ['GET','POST'])
   app.register_error_handler(404,page_not_found)
   app.add_url_rule('/edit_profile','edit_profile',edit_profile,methods= ['GET','POST'])

   # app.add_url_rule('/reset_password_request','reset_password_request',reset_password_request,methods= ['GET','POST'])
   app.add_url_rule('/explore', 'explore', explore)
   return app

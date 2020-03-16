
from datetime import datetime
import time
from hashlib import md5

from werkzeug.security import  generate_password_hash,check_password_hash #用来保护密码，存为哈希值
from flask_login import UserMixin #提供session管理的方法
from flask import current_app
import jwt
from twittor import db, login_manager
from twittor.models.tweet import Tweet

followers = db.Table('followers',
    db.Column ('follower_id', db.Integer,db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),

)

class User(UserMixin,db.Model):#通过继承db.Model创建class User
    id = db.Column (db.Integer , primary_key= True )
    username = db.Column (db.String(64), unique=True ,index = True )#加上index是因为速度会快一些
    email = db.Column(db.String(64),unique= True,index=True)
    password_hash = db.Column(db.String(128))
    about_me= db.Column(db.String(128))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    tweets = db.relationship('Tweet',backref = 'author',lazy='dynamic')#这里的'Tweet'里的,用来了解一个用户发了多少个推特，不是表中的一列

    followed = db.relationship (
        'User',secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy = 'dynamic')

    def __repr__(self):#为了调试方便创建的函数，打印一个实例或者在shell显示
        return 'id={},username={},email={},password_hash={}'.format(
            self.id,self.username ,self.email ,self.password_hash
        )
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    def avatar(self,size = 80):
        md5_digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(md5_digest,size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self,user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count()>0

    def own_and_followed_tweets(self):
        followed = Tweet.query.join(
            followers,(followers.c.followed_id == Tweet.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Tweet.query.filter_by(user_id = self.id)
        return followed.union(own).order_by(Tweet.create_time.desc())

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



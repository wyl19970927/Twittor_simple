from twittor import db
from datetime import datetime



class Tweet(db.Model):
    id = db.Column (db.Integer ,primary_key = True)
    body = db.Column(db.String(140))
    create_time = db.Column(db.DateTime,default= datetime.utcnow)
    user_id = db.Column(db.Integer ,db.ForeignKey('user.id'))#这里的'user,id'里的user不是class那个user而是所建的表的user。user_id必须是user那个table里面的id，所以用ForeignKey关联user里面的id
    def __repr__(self):#为了调试方便创建的函数，打印一个实例或者在shell显示
        return 'id={},body={},create_time={},user_id={}'.format(
            self.id,self.create_time,self.body,self.user_id
        )

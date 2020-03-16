from flask import render_template,redirect,url_for,request,abort,current_app,flash
from flask_login import login_user,current_user,logout_user,login_required
from twittor.forms import LoginForm,RegisterForm,EditProfileForm,TweetForm #,PsaawdResetRequestForm
from twittor.models.user import User,load_user #为了让flask知道这些表存在
from twittor.models.user import Tweet
from twittor import db

@login_required
def index():
   form = TweetForm()
   if form.validate_on_submit(): #如果是http的post
       t = Tweet (body=form.tweet.data, author= current_user)
       db.session.add(t)
       db.session.commit()
       return redirect(url_for('index'))
   name = current_user.username
   page_num = int(request.args.get('page') or 1 )
   tweets = current_user.own_and_followed_tweets().paginate(page=page_num, per_page= current_app.config['TWEET_PER_PAGE'], error_out= False)
   next_url = url_for('index', page = tweets.next_num) if tweets.has_next else None
   prev_url = url_for('index', page=tweets.prev_num) if tweets.has_prev else None
   return render_template('index.html ',name = name,title = 'flask',next_url=next_url,prev_url=prev_url,tweets = tweets.items,form = form)

def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # form1 = Login_Form(csrf_enabled = False)
    form1 = LoginForm()
    if form1.validate_on_submit():
        u = User.query.filter_by(username = form1.username.data).first()
        if u is None or not u.check_password(form1.password.data):#如果账号不存在或者密码不正确
            print('invalid username or passwod')
            return redirect(url_for('login'))
        login_user(u,remember= form1.remember_me.data)
        next_page = request.args.get('next')#作用：在登陆之前可能会点其他入口的页面，在登陆之后会直接跳转到那个页面
        if next_page:
            return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html',title = 'sign in' ,form = form1)
def logout():
    logout_user()
    return redirect(url_for('login'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form2 = RegisterForm()
    if form2.validate_on_submit():#如果form数据合法
        user = User(username=form2.username.data, email=form2.email.data)
        user.set_password(form2.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',tittle = 'Registration',form = form2)

@login_required
def user(username):
    u = User.query.filter_by(username = username).first()
    if u is None:
        abort(404)

    # tweets = Tweet.query.filter_by(author = u)
    # tweets = u.tweets.order_by(Tweet.create_time.desc())
    page_num = int(request.args.get('page') or 1)
    tweets = u.tweets.order_by(Tweet.create_time.desc()).paginate(page=page_num,
                                                                  per_page=current_app.config['TWEET_PER_PAGE'],
                                                                  error_out=False)
    next_url = url_for('profile', page=tweets.next_num, username=username) if tweets.has_next else None
    prev_url = url_for('profile', page=tweets.prev_num, username=username) if tweets.has_prev else None

    if request.method == 'POST':
        if request.form['request_button'] == 'Follow':
            current_user.follow(u)
            db.session.commit()
        else:
            current_user.unfollow(u)
            db.session.commit()

    return render_template('user.html',tittle = 'Profile',next_url=next_url,prev_url=prev_url,tweets = tweets.items ,user = u )
def page_not_found(e):
    return render_template('404.html'),404

@login_required
def edit_profile():
    form = EditProfileForm ()
    if request.method == 'GET':
        form.about_me.data = current_user.about_me
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for('profile', username=current_user.username))
    return render_template('edit_profile.html',form=form)

# def reset_password_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = PsaawdResetRequestForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email = form.email.data).first()
#         if user:
#             flash(
#                 "You should soon receive an email allowing you to reset your \
#                 password. Please make sure to check your spam and trash \
#                 if you can't find the email."
#             )
#         # else:
#         #      raise
#         return redirect(url_for('login'))
#     return render_template('password_reset_request.html', form = form)

def explore():
    page_num = int(request.args.get('page') or 1)
    tweets = Tweet.query.order_by(Tweet.create_time.desc()).paginate(page=page_num,
                                                                  per_page=current_app.config['TWEET_PER_PAGE'],
                                                                  error_out=False)
    next_url = url_for('explore', page=tweets.next_num ) if tweets.has_next else None
    prev_url = url_for('explore', page=tweets.prev_num ) if tweets.has_prev else None


    return render_template('explore.html', tweets=tweets.items,next_url=next_url, prev_url=prev_url,
                          )

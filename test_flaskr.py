# -*- coding: utf-8 -*-
"""
    Flaskr Tests
    ~~~~~~~~~~~~
    Tests the Flaskr application.
    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from threading import Thread
from flask import Flask,render_template,session,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail,Message
import os


app=Flask(__name__)
app.config['SECRET_KEY']="QFCFLASKTEST"
bootstrap = Bootstrap(app)
moment=Moment(app)
#app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///C:/app_folder/flaskr/tests/data.sqlite"
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://steven:qfc23834358@172.18.193.6/flaskr'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
db=SQLAlchemy(app)
mail = Mail(app)
app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[Flasky]'
app.config['FLASKY_MAIL_SENDER']='Flasky Admin <qfcqfcqfc@qq.com>'
app.config['FLASKY_ADMIN']=os.environ.get('FLASKY_ADMIN')
app.config['MAIL_SERVER']='smtp.qq.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWD')

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)
        
def send_email(to,subject,template,**kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
                  sender = app.config['FLASKY_MAIL_SENDER'],recipients = [to])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr

    

"""shell """
from flask_script import Manager, Shell
from flask_migrate import Migrate,MigrateCommand
manager=Manager(app)
migrate=Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)



"""route 路由"""

@app.route('/',methods=["GET","POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known']=False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
        else:
            session['known']=True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),
                           known=session.get('known',False),
                           current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.route('/user/<name>')
def user(name):
    return render_template('index.html',name=name)



"""form 表单"""
from wtforms import StringField,SubmitField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name= StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


"""model 模型"""

class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref = 'role')
    
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>' % self.username

if __name__ == '__main__':
    manager.run()

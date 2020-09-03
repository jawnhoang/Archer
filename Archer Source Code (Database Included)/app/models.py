from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from time import time
import json
from app import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


'''
class to make data table.
'''


@app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


friendsList = db.Table('friends',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), index=True),
                       db.Column('friend_id', db.Integer, db.ForeignKey('user.id')))

block = db.Table('block',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), index=True),
                       db.Column('friend_id', db.Integer, db.ForeignKey('user.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique id per user info
    username = db.Column(db.String(64), index=True, unique=True)  # username for login
    studentName = db.Column(db.String(64), index=True, unique=False)  # Actual Student name
    password = db.Column(db.String(80))
    image_file = db.Column(db.String(64), nullable=False, default = 'default.jpeg')
    email = db.Column(db.String(128), index=True, unique=True)
    surveyVisted = db.Column(db.Boolean)
    seenAtTime = db.Column(db.DateTime)
    reportTally = db.Column(db.Integer)
    reportReason = db.relationship('Report', backref="reason", lazy='dynamic')
    optionSurvey = db.relationship('Survey', backref="person", lazy='dynamic')
    blocked = db.relationship('User', secondary=block,
                              primaryjoin=id == block.c.user_id,
                              secondaryjoin=id == block.c.friend_id,
                              backref=db.backref('block', lazy='dynamic'),
                              lazy='dynamic')
    friends = db.relationship('User', secondary=friendsList,
                              primaryjoin=id == friendsList.c.user_id,
                              secondaryjoin=id == friendsList.c.friend_id,
                              backref=db.backref('friendsList', lazy='dynamic'),
                              lazy='dynamic')
    messageSent = db.relationship('Message', foreign_keys='Message.sender_id',
                                  backref='sender', lazy='dynamic')
    messageRecieved = db.relationship('Message', foreign_keys='Message.recipient_id',
                                      backref='reciever', lazy='dynamic')
    NotificationSender = db.relationship('Notification', foreign_keys='Notification.sender_id',
                                  backref='nSender', lazy='dynamic')
    NotificationReciever = db.relationship('Notification', foreign_keys='Notification.recipient_id',
                                      backref='nReciever', lazy='dynamic')

    def __init__(self, username, studentName, password, email, reportTally):
        self.username = username
        self.studentName = studentName
        self.password = password
        self.email = email
        self.reportTally = reportTally

    def blockUser(self, blocked):
        if blocked not in self.blocked:
            self.blocked.append(blocked)
            return self

    def isBlocking(self, user):
        return self.blocked.filter(block.c.friend_id == user.id).count()>0


    def unBlock(self, friend):
        if friend in self.blocked:
            self.blocked.remove(friend)
            return self


    def befriend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)
            return self

    def unfriend(self, friend):
        if self.isFriendsWith(friend):
            self.friends.remove(friend)
            return self

    def isFriendsWith(self, user):
        return self.friends.filter(friendsList.c.friend_id == user.id).count()>0

    def newMessages(self):
        seenAt = self.seenAtTime or datetime(1900, 1, 1)
        return Message.query.filter_by(reciever=self).filter(Message.timestamp > seenAt).count()


    def __repr__(self):
        return "User(username='{self.username}', " \
               "email='{self.email}', " \
               "password='{self.password}')".format(self=self)


    # Creates a id token that expires in 30 minutes
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    # Takes a token, tries to load the token and returns a user id
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    major = db.Column(db.String(100))
    outdoor = db.Column(db.String(100))
    indoor = db.Column(db.String(100))
    question = db.Column(db.String(80))
    answer = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, major, outdoor, question, answer, indoor, user_id):
        self.major = major
        self.outdoor = outdoor
        self.indoor = indoor
        self.question = question
        self.answer = answer
        self.user_id = user_id

    def __repr__(self):
        return "User(major='{self.major}', " \
               "outdoor='{self.outdoor}', " \
               "indoor='{self.indoor}', " \
               "user_id='{self.user_id}')".format(self=self)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reasonReported = db.Column(db.String(120))
    report_recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, reasonReported, report_recipient_id):
        self.reasonReported = reasonReported
        self.report_recipient_id = report_recipient_id

    def __repr__(self):
        return "User(reasonReported ='{self.reasonReported}')".format(self=self)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(30))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    seenNotif = db.Column(db.Boolean)

    def __init__(self, sender_id, recipient_id, body, seenNotif):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.body = body
        self.seenNotif = seenNotif


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    seenNotif = db.Column(db.Boolean)

    def __init__(self, sender_id, recipient_id, body):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.body = body


    def __repr__(self):
        return '<Message {}>'.format(self.body)









# create database. In case needed to remake database, delete current archer.db
# and run code below
#db.create_all()
#db.session.commit()

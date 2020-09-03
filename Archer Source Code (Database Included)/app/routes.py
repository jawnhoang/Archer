import pickle
import sqlite3
import sys
from aifc import Error

from datetime import datetime
from sqlalchemy import func
from flask import render_template, flash, redirect, url_for, session, request, jsonify
from flask_login import current_user, login_required, login_user, logout_user, UserMixin
from app import db, app  # imported from init__,
from app.form import LoginForm, RegisterForm, SurveyForm, SurveyUpdateForm, \
    MessageForm, RequestResetForm, ResetPasswordForm, ProfileForm, ReportForm, NotificationForm
from app.models import User, Survey, Message, Notification, Report
import os
import secrets

@app.route('/')
def homePage():
    return render_template('Home.html', title = 'Archer')


### ----LOGIN/REGISTRATION CODE ---------------------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if form.password.data == user.password:
                login_user(user, remember=form.remember.data)
                if user.reportTally >= 15 and user.reportTally <20:
                    return redirect(url_for('warning', username = form.username.data))
                elif user.reportTally >=20:
                    return redirect(url_for('deleteAcc'))
                flash('You were logged in')
                if user.surveyVisted == 1:
                    return redirect(url_for('user', username=current_user.username))
                else:
                    return redirect(url_for('survey'))
        flash('Incorrect username/password. Try again.')
    return render_template('Login.html', form=form, title="Login")


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('homePage'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() #Checks if user exists
        question = Survey.query.filter_by(question=form.question.data).first()  # Checks if  question/ans exists
        answer = Survey.query.filter_by(answer=form.answer.data).first() #Checks if  question/ans exists
        if user and question and answer:
            token = user.get_reset_token()
            flash('Sending you to reset password')
            return redirect(url_for('reset_token', token=token))
        else:
            flash('Incorrect input. Try Again.')
    return render_template('ResetRequest.html', title="Password Reset", form=form)



# Required for reset_request to match user
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:

        return redirect(url_for('homePage'))
    user = User.verify_reset_token(token)

    if user is None:  # If the token is wrong or expired
        flash('That is an invalid  or expired token', 'warning')

        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = form.password.data
        user.password = hashed_password
        db.session.commit()
        flash('Your password updated!')

        return redirect(url_for('homePage'))

    return render_template('ResetToken.html', title='Reset Password', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, studentName = form.studentName.data, email=form.email.data, password=form.password.data, reportTally = 0)
        db.session.add(new_user)
        db.session.commit()
        flash('You are now registered!')

        return redirect(url_for('login'))

    return render_template('Registration.html', form=form, title="Register")


### ----LOGIN/REGISTRATION CODE  END---------------------------------------------------------------------------------------

### ----SURVEY CODE ---------------------------------------------------------------------------------------
@app.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    visit = User.query.filter_by(username=current_user.username).first()
    visit.surveyVisted = 1
    form = SurveyForm()
    if form.validate_on_submit():
        option = Survey(major=form.major.data,
                        outdoor=form.outdoor.data,
                        indoor=form.indoor.data,
                        question = form.question.data,
                        answer = form.answer.data,
                        user_id=current_user.id)
        db.session.add(option)
        db.session.commit()

        return redirect(url_for('user', username=current_user.username))

    return render_template('Survey.html', form=form, title="Survey")


@app.route('/survey/updates', methods=['GET', 'POST'])
@login_required
def surveyUpdate():
    personSurvey = Survey.query.filter_by(
        user_id=current_user.id).first()  # finds data connection between survey and user
    form = SurveyUpdateForm()
    if form.validate_on_submit():
        if form.major.data != 'Reselect Major...':
            personSurvey.major = form.major.data
        if form.outdoor.data !='Reselect Outdoor Activity...':
            personSurvey.outdoor = form.outdoor.data
        if form.indoor.data != 'Reselect Indoor Activity...':
            personSurvey.indoor = form.indoor.data
        db.session.commit()
        flash("Activities Updated!")
        return redirect(url_for('user', username=current_user.username))

    return render_template('UpdateSurvey.html', form=form, title="Update Activities")


### ----SURVEY CODE  END---------------------------------------------------------------------------------------

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('AboutUs.html', title="About Us")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('ContactUs.html', title="Contact Us")


### ----PROFILE CODE  ---------------------------------------------------------------------------------------
@app.route('/profile/<username>', methods=['GET', 'POST']) #dashboard
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.surveyVisted == 1:
        personSurvey = Survey.query.filter_by(user_id=current_user.id).first() #Gets your own info
        friendSurvey = Survey.query.filter_by(user_id=user.id).first()    #Gets friend's info
    else:
        return redirect(url_for('survey'))
    image_file = url_for('static', filename = 'profile_pic/' + current_user.image_file)
    return render_template('Dashboard.html',
                           userMajor=personSurvey.major,
                           userOutdoor=personSurvey.outdoor,
                           userIndoor=personSurvey.indoor,
                           user=user,
                           image_file = image_file,
                           title = 'Dashboard')


@app.route('/profile/user_page/<username>') # This is the another users profile page
@login_required
def userProfile(username):
    currUser = User.query.filter_by(username = current_user.username).first()
    user = User.query.filter_by(username=username).first_or_404()
    personSurvey = Survey.query.filter_by(user_id=user.id).first()
    image_file = url_for('static', filename = 'profile_pic/' + user.image_file)
    return render_template('AccountProfile.html',
                           userMajor=personSurvey.major,
                           userOutdoor=personSurvey.outdoor,
                           userIndoor=personSurvey.indoor,
                           user=user, title = 'Archer',
                           image_file = image_file,
                           current_user = currUser)


def save_picture(form_picture): #creates hash for profile pic file
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn= random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route('/profile/<username>/update', methods=['GET', 'POST'])
@login_required
def updateAccount(username):
    form = ProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        if form.username.data:
            current_user.username = form.username.data
        if form.password.data:
            current_user.password = form.password.data
        else:
            form.password = current_user.password
        db.session.commit()
        flash('Account Updated')
        return redirect(url_for('user', username = current_user.username))
    image_file = url_for('static', filename = 'profile_pic/' + current_user.image_file)
    return render_template("UpdateAccount.html", image_file = image_file,
                            form = form)

### ----PROFILE CODE  END---------------------------------------------------------------------------------------
### ----REPORT CODE-----------------------------------------------------------------------
@app.route('/profile/user_page/<username>/report', methods=["GET", "POST"])
def reportUser(username):
    user = User.query.filter_by(username=username).first()
    form = ReportForm()
    if form.validate_on_submit():
        report = Report(reasonReported=form.reasons.data, report_recipient_id = user.id)
        score = user.reportTally #gets report numbers
        if form.reasons.data == 'Harrasment':
            score += 1
            user.reportTally = score
            db.session.commit()
        elif form.reasons.data == 'Illegal Activities':
            score += 3
            user.reportTally = score
            db.session.commit()
        elif form.reasons.data == 'Blackmailing':
            score += 2
            user.reportTally = score
            db.session.commit()
        elif form.reasons.data == 'Harmful/Racist messages':
            score += 5
            user.reportTally = score
            db.session.commit()
        elif form.reasons.data == 'Stalking':
            score += 2
            user.reportTally = score
            db.session.commit()
        db.session.add(report)
        db.session.commit()
        #accountCheck(user.username)
        flash('User has been Reported!')
        return redirect(url_for('user', username=username))
    return render_template('Report.html', user = user, form=form, title = 'Reporting')

### ----REPORT CODE END -------------------------------------------------------------------------------------
### ----BLOCK CODE------------------------------------------------------------------------------------------
@app.route('/block_friend/<username>')
@login_required
def blockUser(username):
    user = User.query.filter_by(username=username).first()
    current_user.blockUser(user)
    db.session.commit()
    flash('Profile Blocked!')
    if current_user.isBlocking(user):
        return redirect(url_for('user', username = username))
    return redirect(url_for('userProfile', username=username,user = user))

@app.route('/unblock_friend/<username>')
@login_required
def unblockUser(username):
    user = User.query.filter_by(username = username).first()
    current_user.unBlock(user)
    db.session.commit()
    flash('Profile Unblocked!')
    return redirect(url_for('userProfile', username=username,user = user))

### ----CHAT CODE ---------------------------------------------------------------------------------------
@app.route('/direct_message', methods=['GET', 'POST'])
@login_required
def chat():
    return render_template('Chat.html')


@app.route('/message/<username>', methods=['GET', 'POST'])
@login_required
def sendMsg(username):
    user = User.query.filter_by(username=username).first_or_404()
    messages = current_user.messageRecieved.order_by(Message.timestamp.desc())
    chatLog = main(current_user.id, user.id)
    form = MessageForm()

    if form.validate_on_submit():
        msg = Message(sender_id=current_user.id, recipient_id=user.id, body=form.message.data)
        sendNotif = Notification(sender_id = current_user.id, recipient_id = user.id, body = 'new message from',
                                seenNotif = 0)
        db.session.add(sendNotif)
        db.session.add(msg)
        db.session.commit()

        flash('Message Sent')

        chatLog = main(current_user.id, user.id)
        i = 0

        return redirect(url_for('sendMsg', username=username, ))
    image_file = url_for('static', filename = 'profile_pic/' + user.image_file)
    return render_template('SendMessage.html', title='Messaging',
                           form=form, user=user,
                           messages=messages, chatLog=chatLog, len=len(chatLog),
                           current_user=current_user,
                           image_file=image_file)


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_task_by_priority(conn, recipient_id,
                            sender_id, ):  # Tasks by priority and fetches all that matches that priority
    cur = conn.cursor()

    # Gets all of sender's/receiver's text
    cur.execute("SELECT  * FROM message as one "
                "JOIN user as two "
                "ON "
                "((one.sender_id=? AND one.recipient_id=?) "
                "OR (one.sender_id=? AND one.recipient_id=?))",
                (sender_id, recipient_id, recipient_id, sender_id,))

    rows = cur.fetchall()

    return rows


def main(receiverCol, senderCol):
    database = r"C:\Users\johnh\Desktop\Archer-jawnhoang-patch-1\archer.db"

    # Create database connection
    conn = create_connection(database)

    chatLog = select_task_by_priority(conn, receiverCol, senderCol)

    with conn:
        return chatLog


### ----CHAT CODE  END---------------------------------------------------------------------------------------

## -----NOTIFICATION CODE-----------------------------------------------------------------------------------
@app.route('/<username>/inbox', methods=['GET', 'POST'])
@login_required
def notifications(username):
    user = User.query.filter_by(username = current_user.username).first() #get current user
    getNotif = Notification.query.filter_by(recipient_id = user.id).order_by(Notification.timestamp.desc())   #get all notif related to user, newest first
    reports = Report.query.filter_by(report_recipient_id = user.id).order_by(Report.id.desc()).first() #most recent report


    form = NotificationForm()
    if form.validate_on_submit():
        if form.seenNotif:
            for x in getNotif:
                x.seenNotif = 1
                db.session.commit()
        return redirect(url_for('notifications', username = current_user.username))
    return render_template('Notification.html', getNotif = getNotif, user=user, reports = reports,
                            form = form,
                            title = 'Inbox')

@app.route('/<username>/accountWarning', methods=["GET", "POST"])
def warning(username):
    user = User.query.filter_by(username = username).first()
    getReasons = Report.query.filter_by(report_recipient_id = user.id).order_by(Report.id.desc())
    getReport = user.reportTally
    return render_template('Warning.html', user = user, getReport=getReport, getReasons=getReasons, title='Notice')

@app.route('/goodbye')
def deleteAcc():
    user = User.query.filter_by(username = current_user.username).first()
    #find all associated data
    userSurvey = Survey.query.filter_by(user_id=user.id).first()
    getNotif = Notification.query.filter_by(recipient_id = user.id).order_by(Notification.timestamp.desc())   #get all notif related to user, newest first
    userMessage = Message.query.filter_by(sender_id = user.id)
    for y in getNotif:
        db.session.delete(y)
    for x in userMessage:
        db.session.delete(x)
    db.session.delete(userSurvey)
    db.session.delete(user)
    db.session.commit()
    return render_template('Goodbye.html', title='Termination')


### ----MATCH CODE ---------------------------------------------------------------------------------------
@app.route('/add_friend/<username>')
@login_required
def addFriend(username):
    user = User.query.filter_by(username=username).first()
    sendNotif = Notification(sender_id = current_user.id, recipient_id = user.id, body = 'new friend request from',
                            seenNotif = 0)
    db.session.add(sendNotif)
    current_user.befriend(user)
    db.session.commit()
    flash('Friend Added!')
    if current_user.isFriendsWith(user):
        return redirect(url_for('user', username = username))
    return redirect(url_for('userProfile', username=username,user = user))

@app.route('/remove_friend/<username>', methods=['GET', 'POST'])
@login_required
def unFriend(username):
    user = User.query.filter_by(username = username).first()
    deleteFriend = current_user.unfriend(user)
    declineFriend = user.unfriend(current_user)
    db.session.commit()
    flash('Friend removed!')
    return redirect(url_for('userProfile', username=username,user = user))

@app.route('/decline_friend/<username>', methods=['GET', 'POST'])
@login_required
def declineFriend(username):
    user = User.query.filter_by(username = username).first()
    declineFriend = user.unfriend(current_user)
    db.session.commit()
    flash('Friend Request Declined!')
    return redirect(url_for('userProfile', username=username,user = user))


@app.route('/profile/majorMatch')
@login_required
def majorMatch():
    # finds relation of current user
    match = Survey.query.filter_by(user_id=current_user.id).first()
    # gets major of current user
    # finds data of all other users with same major
    foundMatch = Survey.query.filter_by(major=match.major)
    # find corresponding link between user_id and user

    return render_template('MatchMajor.html',
                           title="Your Matches by Major",
                           foundMatch=foundMatch,
                           match=match,
                           current_user=current_user)


@app.route('/profile/indoorMatch')
@login_required
def indoorMatch():
    # finds relation of current user
    match = Survey.query.filter_by(user_id=current_user.id).first()
    # gets indoor interests of current user
    match.indoor
    # finds data of all other users with same indoor interests
    foundMatch = Survey.query.filter_by(indoor=match.indoor)

    return render_template('MatchIndoor.html',
                           title="Your Matches by Interests",
                           foundMatch=foundMatch)


@app.route('/profile/outdoorMatch')
@login_required
def outdoorMatch():
    # finds relation of current user
    match = Survey.query.filter_by(user_id=current_user.id).first()
    # gets outdoor interests of current user
    match.outdoor
    # finds data of all other users with same outdoor interests
    foundMatch = Survey.query.filter_by(outdoor=match.outdoor)

    return render_template('MatchOutdoor.html',
                           title="Your Matches by Interests",
                           foundMatch=foundMatch)


### ----MATCH CODE  END---------------------------------------------------------------------------------------


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('homePage'))

from db import Database
from flask import Flask, render_template, redirect, url_for, request, jsonify

app = Flask(__name__)
database = Database(app)

import sqlalchemy
import os
import json
from flask.globals import session
from flask.helpers import flash
from werkzeug.utils import secure_filename
from tweet import Tweets
from user_info import UserInfos
from login import Login
from follower import Followers
from tweet_like import TweetLikes


UPLOAD_FOLDER = './static/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    __remove_session()
    return render_template('sign_up.html')

@app.route('/sign_up', methods = ['POST'])
def sign_up():
    email = request.form['email']
    password = request.form['password']
    if (email is None or email == '') or (password is None or password == ''):
        flash('email or password are not filled')
        return redirect(url_for('home'))

    l = Login()
    try:
        user = l.signup(email, password)
    except sqlalchemy.exc.IntegrityError:
        flash('Duplicate the email, please use another email')
        return redirect(url_for('home'))

    if user:
        __add_session({ 'user_id': user.id, 'email': user.email })
        return redirect(url_for('profile'))
    else:
        flash('The email is exists already')
        return redirect(url_for('login'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == None:
            return redirect(url_for('home'))

        l = Login()
        user = l.login(email, password)
        if user:
            __add_session({
                'user_id': user.id,
                'email': user.email,
                'display_name': user.user_info.display_name,
                'user_name': user.user_info.user_name,
                'age': user.user_info.age,
                'interests': user.user_info.interests,
                'profile_image': user.user_info.profile_image
            })
            return redirect(url_for('tweets'))
        else:
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('sign_up.html')

@app.route('/logout')
def logout():
    __remove_session()
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if session['user_id'] is None:
        return redirect(url_for('home'))

    user_info = UserInfos.search({ 'user_id': session['user_id'] })
    __add_session({
        'user_id': user_info.user_id,
        'display_name': user_info.display_name,
        'user_name': user_info.user_name,
        'age': user_info.age,
        'interests': user_info.interests,
        'profile_image': user_info.profile_image
    })
    return render_template('profile.html')

# @app.route('/profile/new', methods = ['POST'])
# def profile_new():
#     u = UserInfo()
#     id = session['user_id']

#     display_name = request.form['display_name'] or ''
#     user_name = request.form['user_name'] or ''
#     age = request.form['age'] or 0
#     interests = request.form['interests'] or ''
#     u.insert_user_info({ 'user_id': id, 'display_name': display_name, 'user_name': user_name, 'age': age, 'interests': interests})
#     __add_session(u.get_user_info(id))
#     return redirect(url_for('profile'))

@app.route('/profile/<user_id>/edit', methods = ['POST'])
def profile_edit(user_id):
    display_name = request.form['display_name']
    user_name = request.form['user_name']
    age = request.form['age']
    email = request.form['email']
    interests = request.form['interests']

    u = UserInfos.search({ 'user_id': user_id })
    updated = u.update({ 'display_name': display_name, 'user_name': user_name, 'age': age, 'email': email, 'interests': interests})
    __add_session({
        'user_id': updated.user_id,
        'display_name': updated.display_name,
        'user_name': updated.user_name,
        'age': updated.age,
        'interests': updated.interests,
        'profile_image': updated.profile_image,
        'email': updated.user.email
    })
    return redirect(url_for('profile'))

@app.route('/profile/<user_id>/upload_image', methods = ['POST'])
def upload_image(user_id):
    filename = __profile_image(request.files['profile_image'])
    u = UserInfos.search({ 'user_id': user_id })
    u.upload_image(filename)
    __add_session({ 'profile_image': filename })
    return redirect(url_for('profile'))

@app.route('/profile/<user_id>/get_image')
def get_image(user_id):
    u = UserInfos.search({ 'user_id': user_id })
    result = {
        'data': {
            'profile_image': u.get_image()
        }
    }
    return json.dumps(result)

@app.route('/tweets')
def tweets():
    session['tweets'] = Tweets.default_tweets(session['user_id'])
    return render_template('tweet.html')

@app.route('/tweets/new', methods = ['POST'])
def tweets_new():
    t = Tweets({ 'user_id': session['user_id'], 'message': request.form['message'] })
    t.create()
    return redirect(url_for('tweets'))

@app.route('/tweets/<message_id>', methods = ['POST'])
def tweets_edit(message_id):
    t = Tweets.search(message_id)
    tweet = t.invisible()
    return tweet.to_json()

@app.route('/tweets/<message_id>', methods = ['DELETE'])
def tweets_delete(message_id):
    t = Tweets.search(message_id)
    tweet = t.delete()
    return tweet.to_json()

@app.route('/tweets/<message_id>/likes', methods = ['POST'])
def tweet_likes(message_id):
    data = { 'user_id': session['user_id'], 'tweet_id': message_id }
    tl = TweetLikes.search(data)
    if tl:
        v = tl.delete()
    else:
        new = TweetLikes(data)
        v = new.create()
    return v.to_json()

@app.route('/followers/<follow_id>', methods = ['POST'])
def follow(follow_id):
    data = { 'user_id': session['user_id'], 'follow_id': follow_id }
    f = Followers.search(data)
    if f:
        v = f.delete()
    else:
        new = Followers(data)
        v = new.create()
    return v.to_json()

def __add_session(data):
    if 'user_id' in data:
        session['user_id'] = data['user_id']
    if 'email' in data:
        session['email'] = data['email']
    if 'user_info_id' in data:
        session['user_info_id'] = data['user_info_id']
    if 'display_name' in data:
        session['display_name'] = data['display_name']
    if 'user_name' in data:
        session['user_name'] = data['user_name']
    if 'interests' in data:
        session['interests'] = data['interests']
    if 'profile_image' in data:
        session['profile_image'] = data['profile_image']
    if 'age' in data:
        session['age'] = data['age']

def __remove_session():
    session = None

def __allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def __profile_image(file):
    if file and __allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return file.filename

if __name__ == '__main__':
    app.secret_key = 'test'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
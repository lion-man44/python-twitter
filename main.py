from operator import itemgetter
import os
from re import U
from follower import Follower
from tweet_like import TweetLike
from flask.helpers import flash
from werkzeug.utils import secure_filename
from tweet import Tweet
from user_info import UserInfo
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask.globals import session
from login import Login
import json

app = Flask(__name__)

UPLOAD_FOLDER = './static/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    __remove_session()
    session = None
    return render_template('sign_up.html')

@app.route('/sign_up', methods = ['POST'])
def sign_up():
    email = request.form['email']
    password = request.form['password']
    if (email is None or email == '') or (password is None or password == ''):
        flash('email or password are not filled')
        return redirect(url_for('home'))
    l = Login()
    db_id, db_email = l.signup(email, password)
    if db_id:
        session['user_id'] = db_id
        session['email'] = db_email
        return redirect(url_for('tweets'))
    else:
        flash('The email is exists already')
        return redirect(url_for('login'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        l = Login()
        (id, db_email, display_name, user_name, _) = l.login(email, password)
        if email == None:
            return redirect(url_for('sign_up'))
        elif db_email:
            session['user_id'] = id
            session['email'] = db_email
            if display_name is not None:
                session['name'] = display_name
            else:
                session['name'] = user_name
            return redirect(url_for('tweets'))
        else:
            return redirect(url_for('sign_up'))
    elif request.method == 'GET':
        return render_template('sign_up.html')

@app.route('/logout')
def logout():
    __remove_session()
    return redirect(url_for('login'))

@app.route('/chosing_link')
def chosing_link():
    if session['name'] is not None:
        name = session['name']
    else:
        name = session['email']
    return render_template('chosing_link.html', name = name)

@app.route('/profile')
def profile():
    if session['user_id'] is None:
        return redirect(url_for('home'))
    u = UserInfo()
    id = session['user_id']
    user = u.get_user_info(id)
    __add_session(user)
    return render_template('profile.html')

@app.route('/profile/new', methods = ['POST'])
def profile_new():
    u = UserInfo()
    id = session['user_id']

    display_name = request.form['display_name'] or ''
    user_name = request.form['user_name'] or ''
    age = request.form['age'] or 0
    interests = request.form['interests'] or ''
    u.insert_user_info({ 'user_id': id, 'display_name': display_name, 'user_name': user_name, 'age': age, 'interests': interests})
    __add_session(u.get_user_info(id))
    return redirect(url_for('profile'))

@app.route('/profile/<user_id>/edit', methods = ['POST'])
def profile_edit(user_id):
    u = UserInfo()
    id = user_id

    display_name = request.form['display_name']
    user_name = request.form['user_name']
    age = request.form['age'] or 0
    email = request.form['email']
    interests = request.form['interests']

    u.update_user_info({ 'id': id, 'display_name': display_name, 'email': email, 'user_name': user_name, 'age': age, 'interests': interests})
    __add_session(u.get_user_info(id))
    return redirect(url_for('profile'))

@app.route('/profile/<user_id>/upload_image', methods = ['POST'])
def upload_image(user_id):
    u = UserInfo()
    filename = __profile_image(request.files['profile_image'])
    u.update_profile_image(user_id, filename)
    __add_session_only_profile_image(filename)
    return redirect(url_for('profile'))

@app.route('/profile/<user_id>/get_image')
def get_image(user_id):
    u = UserInfo()
    result = {
        'data': {
            'profile_image': u.get_profile_image(user_id)
        }
    }
    return json.dumps(result)

@app.route('/tweets')
def tweets():
    t = Tweet()
    session['tweets'] = t.get_tweets({ 'user_id': session['user_id'] })
    return render_template('tweet.html')

@app.route('/tweets/new', methods = ['POST'])
def tweets_new():
    id = session['user_id']

    message = request.form['message']
    t = Tweet()
    t.add_tweet({ 'user_id': id, 'message': message })
    return redirect(url_for('tweets'))

@app.route('/tweets/<message_id>', methods = ['POST'])
def tweets_edit(message_id):
    t = Tweet()
    if t.invisible_tweet(message_id):
        result = {
            'code': 200,
            'message': 'OK'
        }
    else:
        result = {
            'code': 503,
            'message': 'It happened something'
        }
    return jsonify(values = json.dumps(result))

@app.route('/tweets/<message_id>', methods = ['DELETE'])
def tweets_delete(message_id):
    t = Tweet()
    if t.delete_tweet(message_id):
        result = {
            'code': 200,
            'message': 'OK'
        }
    else:
        result = {
            'code': 503,
            'message': 'It happened something'
        }
    return jsonify(values = json.dumps(result))

@app.route('/tweets/<message_id>/likes', methods = ['POST'])
def tweet_likes(message_id):
    tl = TweetLike()
    if tl.favorite(message_id, session['user_id']):
        result = {
            'code': 200,
            'message': 'OK'
        }
    else:
        result = {
            'code': 503,
            'message': 'It happened something'
        }
    return json.dumps(result)

@app.route('/followers/<follow_id>', methods = ['POST'])
def follow(follow_id):
    user_id = session['user_id']
    f = Follower()
    if f.follow(user_id, follow_id):
        result = {
            'code': 200,
            'message': 'OK'
        }
    elif f.unfollow(user_id, follow_id):
        result  = {
            'code': 200,
            'message': 'OK'
        }
    else:
        result = {
            'code': 503,
            'message': 'It happened something'
        }
    return json.dumps(result)
       
def __add_session_only_profile_image(filename):
    session['profile_image'] = filename

def __add_session(data):
    id, email, user_info_id, display_name, user_name, age, interests, profile_image = data
    session['user_id'] = id
    session['email'] = email
    session['user_info_id'] = user_info_id
    session['display_name'] = display_name
    session['user_name'] = user_name
    session['interests'] = interests
    session['profile_image'] = profile_image
    session['age'] = age

def __remove_session():
    for key in session:
        session[key] = None

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

# A very simple Flask Hello World app for you to get started with...

from flask import Flask,request, redirect, render_template, session, make_response
from flask_session import Session
import json
import s3util
import uuid
import dbutil
from datetime import datetime

app = Flask(__name__)

app.config['SESSION_PERMANENT']= False
app.config['SESSION_TYPE']= 'filesystem'
Session(app)

def auto_login():
    cookie = request.cookies.get('remember')
    if cookie is None:
        return False

    table = dbutil.get_table('Remember')
    result = table.get_item(Key={'key':cookie})
    if 'Item' not in result:
        return False

    remember = result['Item']
    table = dbutil.get_table('Users')
    result = table.get_item(Key={'email':remember['email']})

    user = result['Item']

    #login user
    session['email'] = user['email']
    session['username'] = user['UserName']
    return True

def is_logged_in():
    if not session.get('email'):
        return auto_login()
    return True

@app.route('/home.html')
def home():
    if not is_logged_in():
        return redirect('/login.html')
    user = dbutil.find_user(session['email'])
    return render_template('home.html', username=session['username'], profilepic=user['ProfilePic'])

@app.route('/account/<username>')
def account(username):
    if 'username' not in session: return redirect('/login.html')
    user = dbutil.find_username(username)
    if session['username'] == username:
        return render_template('home.html', username=username, profilepic=user['ProfilePic'])
    return render_template('account.html', username=username, profilepic=user['ProfilePic'])

@app.route('/logout.html')
def logout():
    session.pop('email', None)
    session.pop('username', None)

    response = make_response(redirect('/login.html'))
    response.delete_cookie('remember')
    return response

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/feed.html')
def feedpage():
    return render_template('feed.html')

@app.route('/signup')
def trysignup():
    username = request.args.get('username', '')
    email = request.args.get('email', '')
    password = request.args.get('password', '')

    if username == '' or password =='':
        return {'result':'Username and Password required'}

    if dbutil.find_user(email) is not None:
        return {'result': 'Email already in use'}

    if '@' not in email or '.' not in email:
        return {'result': 'Invalid Email format'}

    dbutil.add_user(email, username, password)

    session['email'] = email
    session['username'] = username

    return {'result':'OK'}

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/login')
def trylogin():
    email = request.args.get('email', '')
    password = request.args.get('password', '')
    if email == '' or password =='':
        return {'result':'Bad Login'}

    table = dbutil.get_table('Users')
    item = table.get_item(Key={'email':email})
    if 'Item' not in item:
        return {'result': 'Email not found'}

    user = item['Item']
    if password != user['Password']:
        return {'result': 'Invalid password'}

    session['email'] = user['email']
    session['username'] = user['UserName']
    response = make_response({'result':'OK'})

    remember = request.args.get('remember', 'no')
    if(remember == 'no'):
        response.delete_cookie('remember')
    else:
        key = dbutil.add_remember_key(user['email'])
        response.set_cookie('remember',key,60*60*24*14) #Remember for 14 days
    return response

@app.route('/postitems')
def postitems():
    username = request.args.get('username', None)

    if username:
        results = dbutil.loadpostsbyusername(username)
    else:
        results = dbutil.post_items()

    if not username:
        results = results[:10]
    return {'result': results}

@app.route('/addpost')
def addpost():
    if not is_logged_in():
        return {'result': 'Not logged in'}

    text = request.args.get('text', '')
    now = datetime.now()
    data = now.strftime("%Y %m %d %H:%M.%S")

    username = session['username']
    if text == '':
        return {'result': 'Title and Text required'}

    dbutil.add_post(username,text, data)
    return {'result': 'OK'}

@app.route('/addreply')
def addreply():
    if not is_logged_in():
        return {'result': 'Not logged in'}

    post_id = request.args.get('postid', '')
    text = request.args.get('text', '')
    now = datetime.now()
    data = now.strftime("%Y %m %d %H:%M.%S")

    username = session['username']
    if post_id == '' or text == '':
        return {'result': 'Text and Post ID required'}

    dbutil.add_post(username, text, data, post_id)
    return {'result': 'OK'}

@app.route('/listreplies')
def listreplies():
    postid = request.args.get('postid', '')

    if postid == '':
        return {'result': []}

    replies = dbutil.loadreplies(postid)
    return {'result': replies}

@app.route('/deletepost')
def deletepost():
    if not is_logged_in():
        return {'result': 'Not logged in'}

    post_id = request.args.get('postid', '')

    if post_id == '':
        return {'result': 'Post ID is required'}

    dbutil.delete_post(post_id)
    return redirect('/home.html')

@app.route('/post/<postid>')
def post(postid):
    p = dbutil.get_post(postid)

    if p is None:
        return {'result': 'Post not found'}

    return render_template('post.html', p=p)

@app.route('/account.html')
def account_redirect():
    if not is_logged_in():
        return redirect('/login.html')
    user = dbutil.find_user(session['email'])
    return render_template('account.html', username=session['username'], profilepic=user['ProfilePic'])

@app.route('/listfiles')
def listfiles():
    return s3util.listfiles()

@app.route('/uploadfile', methods=['POST'])
def uploadfile():
    file = request.files["file"]
    filename = file.filename

    ct = 'image/jpeg'
    if filename.endswith('png'):
        ct = 'image/png'

    filename = str(uuid.uuid4()) + '_' + filename
    bucket = s3util.get_public_bucket()
    bucket.upload_fileobj(file, filename, ExtraArgs={'ContentType': ct})
    dbutil.update_user_pic(session['email'], filename)

    return {'results' : 'OK'}

@app.route('/listitems')
def listitems():
    results = dbutil.list_items()
    return {'result':results, 'url': s3util.STORAGE_URL}
# Server file for server lab (server.py)
# By: Will Chau

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os.path
from sqlalchemy.exc import SQLAlchemyError
from models import db, Message, User
from datetime import datetime
import requests

#error codes
SUCCESS = "1"
USER_EXISTS_IN_DB = "10"
USER_DOES_NOT_EXIST = "11"
AUTHENTICATION_FAILED = "12"

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages_db.sqlite'

db.init_app(app)
db.create_all(app=app)

def check_username_password(username, password):
    '''Given a username and password, will return a SUCCESS code if
    the username and password is correct, otherwise will return a
    PASSWORD_INCORRECT code'''
    try:
        query = User.query.filter_by(username=username, password=password).first()
        #if not found in db
        if query is not None:
            return SUCCESS
        else:
            return AUTHENTICATION_FAILED

    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error

def get_server_address(username):
    """Gets the server address for a given username (a bot) if one
    exists. Otherwise, returns None.
    """
    try:
        query = User.query.filter_by(username=username).first()
        if query:
            return query.server_address
        else:
            return None
    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error


def save_message_to_db(sender, recipient, message, timestamp):
    '''Given a sender, recipient, message and timestamp, adds a message
    record to the database. Returns a SUCCESS code if it was successful,
    otherwise, it will return a SQLAlchemy error'''
    try:
        query = Message(sender=sender, recipient=recipient, message=message,timestamp=timestamp)
        db.session.add(query)
        db.session.commit()
        return SUCCESS

    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error

def register_user_to_db(username, password, server_address=None):
    '''Given a username and password, adds a user record in the database.
    Returns a SUCCESS code if it was successful, otherwise, it will
    return a SQLAlchemy error'''
    try:
        query = User(username=username, password=password, server_address=server_address)
        db.session.add(query)
        db.session.commit()
        return SUCCESS

    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error

def edit_registration_in_db(username, new_password=None, new_server_address=None):
    """Given a username, edits the record for that username with a new
    password and/or server address if they are provided.
    """
    try:
        query = User.query.filter_by(username=username).first()
        if new_password:
            query.password = new_password
        if new_server_address:
            query.server_address = new_server_address
        db.session.commit()
        return SUCCESS
    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error

def find_user_from_db(username):
    '''Given a username, finds that username in the database. If the
    username is not found, returns false, otherwise, it will return a SQLAlchemy error'''
    try:
        query = User.query.filter_by(username=username).first()
        if not query:
            return USER_DOES_NOT_EXIST
        else:
            return USER_EXISTS_IN_DB

    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error

def get_messages_from_db(person):
    '''Give a person's username, gets all the messages sent to that
    person and returns a list of messages even if there are no messages.
    Each message is stored in a dictionary based on the Message Model.'''
    try:
        query = Message.query.filter_by(recipient=person).all()
        messageList = []
        for row in query:
            row_as_dict = row.__dict__
            row_as_dict.pop('_sa_instance_state', None)
            messageList.append(row_as_dict)
        return {"messages": messageList}

    except SQLAlchemyError as e:
      error = str(e.__dict__['orig'])
      return error
     
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    server_address = data['server_address']

    if find_user_from_db(username) == USER_DOES_NOT_EXIST:
        register_user_to_db(username, password, server_address)
        return SUCCESS
    else:
        return USER_EXISTS_IN_DB

@app.route('/ping', methods=['GET'])
def ping():
    return SUCCESS

@app.route('/auth', methods=['GET'])
def authenticate():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if find_user_from_db(username) == USER_DOES_NOT_EXIST:
        return USER_DOES_NOT_EXIST
    else:
        return check_username_password(username, password)

@app.route('/', methods=['POST'])
def send_message():
    data = request.get_json()
    sender = data['sender']
    recipient = data['recipient']
    message = data['message']
    timestamp = data['timestamp']
    if find_user_from_db(recipient) == USER_DOES_NOT_EXIST:
        return (USER_DOES_NOT_EXIST, 400)
    else:
        server_address = get_server_address(recipient)
        if server_address:
            server_address = server_address + '/message'
            payload = {
                    'sender': sender,
                    'msg': message,
                    'timestamp': timestamp
                    }
            r = requests.post(server_address, json=payload)
            if r.ok:
                return save_message_to_db(recipient, sender, r.json()["msg"], timestamp)
            else:
                try:
                    errors = r.json()["errors"]
                except:
                    errors = r.reason
                response = "Error recieved while contacting bot: {} - {}".format(r.status_code, errors)
                return (response, 503)
        else:
            return save_message_to_db(sender, recipient, message, timestamp)

@app.route('/get_messages', methods=['GET'])
def get_messages():
    data = request.get_json()
    person = data['username']
    return get_messages_from_db(person)

@app.route('/edit', methods=['POST'])
def edit_registration():
    data = request.get_json()
    username = data['username']
    old_password = data['old_password']
    new_password = data['new_password']
    server_address = data['server_address']

    if find_user_from_db(username) == USER_DOES_NOT_EXIST:
        return USER_DOES_NOT_EXIST
    else:
        auth = check_username_password(username, old_password)
        if auth:
            return edit_registration_in_db(username, new_password, server_address)
        else:
            return auth

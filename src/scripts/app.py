from flask import Flask, request, jsonify, session, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db')

# Create tables if they do not exist

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create tables if they do not exist
with app.app_context():
    db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_user = User(username=data['username'], password=hashed_password, role=data.get('role', 'user'))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'registered successfully'})
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'login failed'})
        login_user(user)
        return render_template('home.html', channels=Channel.query.all(), users=User.query.all(), current_user=current_user)
    return render_template('login.html')

@app.route('/channels')
def channels():
    channels = Channel.query.all()
    return render_template('channels.html', channels=channels)

@app.route('/dm')
def dm():
    users = User.query.all()
    return render_template('dm.html', users=users)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'logged out successfully'})

@app.route('/protected')
@login_required
def protected():
    return jsonify({'message': 'This is a protected route'})

@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        return jsonify({'message': 'You do not have access to this route'}), 403
    return jsonify({'message': 'Welcome to the admin route'})

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    receiver = User.query.filter_by(username=data['receiver']).first()
    if not receiver:
        return jsonify({'message': 'Receiver not found'}), 404
    new_message = Message(sender_id=current_user.id, receiver_id=receiver.id, content=data['content'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully'})

@app.route('/get_messages', methods=['GET'])
@login_required
def get_messages():
    messages = Message.query.filter((Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)).all()
    output = []
    for message in messages:
        sender = User.query.get(message.sender_id)
        receiver = User.query.get(message.receiver_id)
        output.append({
            'sender': sender.username,
            'receiver': receiver.username,
            'content': message.content,
            'timestamp': message.timestamp
        })
    return jsonify({'messages': output})

@app.route('/channel_messages', methods=['GET'])
@login_required
def channel_messages():
    channel_name = request.args.get('channel')
    channel = Channel.query.filter_by(name=channel_name).first()
    if not channel:
        return jsonify({'message': 'Channel not found'}), 404
    messages = Message.query.filter_by(receiver_id=channel.id).all()
    output = []
    for message in messages:
        sender = User.query.get(message.sender_id)
        output.append({
            'sender': sender.username,
            'content': message.content,
            'timestamp': message.timestamp
        })
    return jsonify({'messages': output})

@app.route('/dm_messages', methods=['GET'])
@login_required
def dm_messages():
    username = request.args.get('user')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    messages = Message.query.filter((Message.sender_id == current_user.id) & (Message.receiver_id == user.id) | (Message.sender_id == user.id) & (Message.receiver_id == current_user.id)).all()
    output = []
    for message in messages:
        sender = User.query.get(message.sender_id)
        output.append({
            'sender': sender.username,
            'content': message.content,
            'timestamp': message.timestamp
        })
    return jsonify({'messages': output})

@app.route('/send_channel_message', methods=['POST'])
@login_required
def send_channel_message():
    data = request.get_json()
    channel = Channel.query.filter_by(name=data['channel']).first()
    if not channel:
        return jsonify({'message': 'Channel not found'}), 404
    new_message = Message(sender_id=current_user.id, receiver_id=channel.id, content=data['content'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully'})

@app.route('/send_dm_message', methods=['POST'])
@login_required
def send_dm_message():
    data = request.get_json()
    receiver = User.query.filter_by(username=data['receiver']).first()
    if not receiver:
        return jsonify({'message': 'Receiver not found'}), 404
    new_message = Message(sender_id=current_user.id, receiver_id=receiver.id, content=data['content'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully'})

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.form
    hashed_password = generate_password_hash('defaultpassword', method='pbkdf2:sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return 'User created', 200

@app.route('/create_channel', methods=['POST'])
def create_channel():
    data = request.get_json()
    new_channel = Channel(name=data['channel_name'])
    db.session.add(new_channel)
    db.session.commit()
    return jsonify({'message': 'Channel created'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


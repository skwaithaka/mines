from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from main import database, login_manager, app,SECURITY_PASSWORD_SALT
from flask_login import UserMixin
from flask_login import current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    phone_number = database.Column(database.String(120), unique=True, nullable=False)
    image_file = database.Column(database.String(20), nullable=False, default='default.jpg')
    activated = database.Column(database.Boolean, nullable=False, default=False)
    confirmed = database.Column(database.Boolean, nullable=False, default=False)
    popularity = database.Column(database.Boolean, nullable=False, default=False)
    password = database.Column(database.String(60), nullable=False)
    products = database.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    



    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def generate_confirmation_token(email):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps(email, salt='email-confirm')


    def confirm_token(token, expiration=3600):
        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt='email-confirm',
                max_age=expiration
            )
        except:
            return False
        return email



    def __repr__(self):
        return f"User('{self.username}', '{self.activated}', '{self.confirmed}')"

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    date_posted = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    content = database.Column(database.Text, nullable=False)
    location = database.Column(database.Text, nullable=False)
    price = database.Column(database.Integer,nullable=False, default=0)
    category = database.Column(database.Text, nullable=False,default='others')
    image_file1 = database.Column(database.Text, nullable=False, default='default.png')
    image_file2 = database.Column(database.Text, nullable=False, default='default.png')
    image_file3 = database.Column(database.Text, nullable=False, default='default.png')
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.image_file1}' ,  '{self.category}' , '{self.location}')"





















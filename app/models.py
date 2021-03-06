from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref="author", lazy="dynamic")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    @login.user_loader
    def load_user(id: str):
        return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(128), index=True)
    description = db.Column(db.String(512), index=True)
    file_path = db.Column(db.String(256))
    likes = db.relationship('PostLikes', backref="liked", lazy="dynamic")

    def like_amount(self):
        return self.likes.count()

    def do_user_like(self, user_id: int):
        return self.likes.filter_by(user_id=user_id).first() is not None


class PostLikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer)

    def do_user_like(self, id: int):
        return self.user_id == id

from .extensions import db
from flask_login import UserMixin # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash

# Association table for the many-to-many relationship between Users and Server
server_operator = db.Table('server_operator',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('server_id', db.Integer, db.ForeignKey('server.id'), primary_key=True)
)

class BaseModel(db.Model):
    __abstract__ = True
    __allow_unmapped__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Users(UserMixin, BaseModel):
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash  = db.Column(db.Text(), nullable=False)
    profile_image = db.Column(db.String(80), nullable=True, default='default.jpg')
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    # one to many Relationship with Blog
    # Blog 모델에서 author로 접근 가능, User 모델에서 blogs로 접근 가능
    blogs = db.relationship('Blog', backref='author', lazy=True)
    # many to many Relationship with Server
    servers = db.relationship('Server',
                              secondary=server_operator,
                              back_populates='operators',
                              lazy='dynamic')

    def set_password(self, password):
        self.password_hash  = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Users {self.username}>'
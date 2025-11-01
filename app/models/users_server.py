from ..extensions import db
from flask_login import UserMixin # type: ignore
from sqlalchemy.dialects.postgresql import INET
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(db.Model):
    __abstract__ = True
    __allow_unmapped__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

# Association table for the many-to-many relationship between Users and Servers
class ServerUser(BaseModel):
    __tablename__ = 'users_servers'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'))

class Users(UserMixin, BaseModel):
    __tablename__ = 'users'
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password  = db.Column(db.Text(), nullable=False)
    profile_image = db.Column(db.String(80), nullable=True, default='default.jpg')
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    # many to many Relationship with Server
    allowed_servers = db.relationship('Server', secondary='users_servers',
                        backref='operators', lazy='dynamic')

    def set_password(self, password):
        self.password  = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Users {self.username}>'

class Server(BaseModel):
    __tablename__ = 'servers'
    server_name = db.Column(db.String(30), unique=True, nullable=False)
    login_id = db.Column(db.String(100), nullable=False)
    ip_addr = db.Column(INET, nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    port = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    id_ip = db.Column(db.String(20))

    def __init__(self, server_name, ip_addr, login_id,  **kwargs):
        super().__init__(server_name=server_name, ip_addr=ip_addr, login_id=login_id, **kwargs)
        if not self.port:
            self.port = 22
        if not self.id_ip:
            self.id_ip = f"{self.login_id}@{self.ip_addr}"

    # SV_INFO와 one to one Relationship
    # sv_info = db.relationship('SV_INFO', backref='server', uselist=False, lazy=True)

    def __repr__(self):
        return f'<Server {self.id_ip}>'
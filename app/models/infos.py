from ..extensions import db
from sqlalchemy.dialects.postgresql import INET # type: ignore
from werkzeug.security import generate_password_hash
from .users_servers import BaseModel

# class SV_INFO(BaseModel):
#     hostname = db.Column(db.String(255), nullable=False, unique=True)
#     ip_address = db.Column(INET, nullable=False, unique=True)
#     os_info = db.Column(db.String(255), nullable=False)
#     uptime = db.Column(db.String(100), nullable=False)
#     checked_date = db.Column(db.DateTime, default=db.func.current_timestamp())
#     # server와 one to one Relationship
#     sv_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False, unique=True)
#     # Resources_info와 one to many Relationship
#     resources_infos = db.relationship('Resources_info', backref='sv_info', lazy=True)
#     # Sysctl_info와 one to many Relationship
#     sysctl_infos = db.relationship('Sysctl_info', backref='sv_info', lazy=True)

#     def __repr__(self):
#         return f'<Server {self.hostname} for {self.ip_address}>'

# class Resources_info(BaseModel):
#     free_memory = db.Column(db.String(12), nullable=False)
#     cpu_cores = db.Column(db.String(12), nullable=False)
#     cpu_usage = db.Column(db.String(12), nullable=False)
#     disk_usage = db.Column(db.Text, nullable=False)
#     custom_1 = db.Column(db.String(12))
#     custom_2 = db.Column(db.String(12))
#     custom_3 = db.Column(db.String(12))
#     custom_4 = db.Column(db.String(12))
#     checked_date = db.Column(db.DateTime, default=db.func.current_timestamp())
#     # SV_INFO와 one to many Relationship
#     sv_info_id = db.Column(db.Integer, db.ForeignKey('sv_info.id'), nullable=False)

#     def __repr__(self):
#         return f'<Server {self.sv_info.hostname} By {self.sv_info.ip_address}>'

# class Sysctl_info(BaseModel):
#     swappiness = db.Column(db.String(12))
#     dirty_ratio = db.Column(db.String(12))
#     dirty_background_ratio = db.Column(db.String(12))
#     overcommit_memory = db.Column(db.String(12))
#     overcommit_ratio = db.Column(db.String(12))
#     custom_1 = db.Column(db.String(12))
#     custom_2 = db.Column(db.String(12))
#     custom_3 = db.Column(db.String(12))
#     custom_4 = db.Column(db.String(12))
#     checked_date = db.Column(db.DateTime, default=db.func.current_timestamp())
#     # SV_INFO와 one to many Relationship
#     sv_info_id = db.Column(db.Integer, db.ForeignKey('sv_info.id'), nullable=False)

#     def __repr__(self):
#         return f'<Server {self.sv_info.hostname} By {self.sv_info.ip_address}>'
from ..extensions import db
from sqlalchemy.dialects.postgresql import INET # type: ignore
from werkzeug.security import generate_password_hash
from .users import BaseModel

class SvInfo(BaseModel):
    __tablename__ = 'sv_infos'
    name = db.Column(db.String(50), nullable=False)
    os_info = db.Column(db.String(100), nullable=False)
    total_memory = db.Column(db.String(12), nullable=False)
    cpu_info = db.Column(db.Text, nullable=False)
    cpu_cores = db.Column(db.String(12), nullable=False)
    uptime = db.Column(db.String(100), nullable=False)

    checked_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    # HostnameIp와 one to many Relationship
    hostname_ip_id = db.Column(db.Integer, db.ForeignKey('hostname_ips.id'), nullable=False)
    
    def __repr__(self):
        return f'<Server {self.name} By {self.hostname_ip.hostname}>'

from ..extensions import db
from sqlalchemy.dialects.postgresql import INET # type: ignore
from .users import BaseModel

# server와 one to one Relationship
class HostInfos(BaseModel):
    __tablename__ = 'host_infos'

    hostname = db.Column(db.String(20), nullable=False, unique=True)
    ip_address = db.Column(INET, nullable=False, unique=True)

    # Servers와 one to one Relationship
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'))

    # SvInfo와 one to many Relationship
    # sv_infos = db.relationship('SvInfo', backref='hostname', lazy=True)
    # SVSysctl와 one to many Relationship
    # sv_sysctls = db.relationship('SVSysctl', backref='server_info', lazy=True)

    def __repr__(self):
        return f'<HostInfos {self.hostname} for {self.ip_address}>'

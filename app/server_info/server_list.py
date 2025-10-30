from ..extensions import db
from ..models_server import SV_SSH as Server

def get_servers_from_db():
    servers = db.session.query(Server).all()
    # servers = .query.all()
    server_list = []
    for server in servers:
        server_list.append({
            'server_name': server.server_name,
            'ip_addr': server.server_ip,
            # 'username': server.username,
            'username': 'root',
            # 'password': server.password, 
            'password': 1, 
            'port': 22
        })
    return server_list
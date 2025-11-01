import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app
from app.extensions import db
from app.models.users_server import Users, Server

def seed_data():
    """Seeds the database with initial data."""
    app = create_app()
    with app.app_context():
        # Check if data already exists to prevent duplicates
        if Users.query.first() is not None or Server.query.first() is not None:
            print("Database already contains data. Skipping seeding.")
            return

        print("Seeding database...")
        s1 = Server(server_name='R6', login_id='root', ip_addr='192.168.219.206', port=22, password='1')
        s2 = Server(server_name='R7', login_id='root', ip_addr='192.168.219.7', port=22,password='1')
        s3 = Server(server_name='R8', login_id='root', ip_addr='192.168.219.111', port=22,password='1')
        s4 = Server(server_name='R9', login_id='root', ip_addr='192.168.219.209', port=22,password='1')

        admin = Users(username='admin', email='admin@demo.com', is_admin=True)
        admin.set_password('admin')

        op_kim = Users(username='op_kim', email='op_kim@demo.com')
        op_kim.set_password('1111')

        op_woo = Users(username='op_woo', email='op_woo@demo.com')
        op_woo.set_password('1111')

        test = Users(username='test', email='test@demo.com')
        test.set_password('1111')

        kalpa = Users(username='kalpa', email='kalpa@demo.com', is_admin=True)
        kalpa.set_password('1111')

        db.session.add_all([s1, s2, s3, s4, admin, op_kim, op_woo, test, kalpa])
        db.session.commit()

        admin.allowed_servers.extend([s1, s2, s3, s4])
        op_kim.allowed_servers.extend([s1, s2])
        op_woo.allowed_servers.extend([s3, s4])
        test.allowed_servers.append(s1)

        db.session.commit()
        print("Database seeded successfully.")

if __name__ == '__main__':
    seed_data()

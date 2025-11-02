import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app
from app.extensions import db
from app.models.servers import Servers
from app.models.users import Users

def seed_data():
    """Seeds the database with initial data."""
    app = create_app()
    with app.app_context():
        # Check if data already exists to prevent duplicates
        admin = db.session.query(Users).filter_by(username='admin').first()
        op_kim = db.session.query(Users).filter_by(username='op_kim').first()
        op_woo = db.session.query(Users).filter_by(username='op_woo').first()
        test = db.session.query(Users).filter_by(username='test').first()
        kalpa = db.session.query(Users).filter_by(username='kalpa').first()

        s1 = db.session.query(Servers).filter_by(server_name='R6').first()
        s2 = db.session.query(Servers).filter_by(server_name='R7').first()
        s3 = db.session.query(Servers).filter_by(server_name='R8').first()
        s4 = db.session.query(Servers).filter_by(server_name='R9').first()

        admin.allowed_servers.extend([s1, s2, s3, s4])
        kalpa.allowed_servers.extend([s1, s2, s3, s4])
        op_kim.allowed_servers.extend([s1, s2])
        op_woo.allowed_servers.extend([s3, s4])
        test.allowed_servers.append(s1)

        db.session.commit()
        print("Database seeded successfully.")

if __name__ == '__main__':
    seed_data()

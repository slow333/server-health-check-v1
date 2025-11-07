import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app
from app.extensions import db
from app.models.commands import Commands

def seed_data():
    """Seeds the database with initial data."""
    app = create_app()
    with app.app_context():
        # Check if data already exists to prevent duplicates
        # if db.session.query(Commands).first():
        #     print("Data already exists. Skipping seeding.")
        #     return

        print("Seeding database...")
        commands = [
            Commands(category='host_info', name='hostname', cmd='hostname;'),
            Commands(category='host_info', name='ip_address', cmd='hostname -I;'),
            Commands(category='sv_info', name='os_version', cmd='uname -a'),
            Commands(category='sv_info', name='top_Info', cmd='top -b -n1'),
            Commands(category='sv_info', name='total_memory', cmd="free -m  | awk 'NR==2{print $2}';"),
            Commands(category='sv_info', name='total_swap', cmd="free -m  | awk 'NR==3{print $2}';"),
            Commands(category='sv_info', name='cpu_cores', cmd='grep -c processor /proc/cpuinfo;'),
            Commands(category='sv_info', name='free_memory', cmd="free -m  | awk 'NR==2 {print (($4+$6)/$2)*100 }';"),
            Commands(category='sv_info', name='cpu_usage', cmd="vmstat 1 1 | tail -n 1 | awk '{print $13}';"),
            Commands(category='sv_info', name='disk_usage', cmd='df -h;'),
            Commands(category='sv_info', name='uptime', cmd='uptime;'),
            Commands(category='sv_info', name='checked_date', cmd="date '+%Y-%m-%d %H:%M';"),

            Commands(category='sv_sysctl', name='vm.swappiness', cmd='sysctl vm.swappiness;'),
            Commands(category='sv_sysctl', name='vm.dirty_ratio', cmd='sysctl vm.dirty_ratio;'),
            Commands(category='sv_sysctl', name='vm.dirty_background_ratio', cmd='sysctl vm.dirty_background_ratio;'),
            Commands(category='sv_sysctl', name='vm.overcommit_memory', cmd='sysctl vm.overcommit_memory;'),
            Commands(category='sv_sysctl', name='vm.overcommit_ratio', cmd='sysctl vm.overcommit_ratio;'),
        ]

        db.session.add_all(commands)
        db.session.commit()
        print("Database seeded successfully.")

if __name__ == '__main__':
    seed_data()

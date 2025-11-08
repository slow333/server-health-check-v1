from flask import (
  Blueprint, redirect, 
  render_template as render, flash, url_for) # type: ignore
from flask_login import current_user, login_required
from ..extensions import db
from ..models.users import Users
from ..models.servers import Servers
from ..models.hostinfos import HostInfos
from .pagenation import pagenation
from .get_data.get_sar_traffic import get_sar_traffic
import os
import re
from sqlalchemy import or_, and_ # type: ignore
# hostname,IP,Interface,Date Time,rxpck/s,txpck/s,rxkB/s,txkB/s

bp = Blueprint("sar_traffic", __name__, url_prefix="/health/sar_traffic")

@bp.route("/generate")
@login_required
def generate_traffic():
    sar_traffic = get_sar_traffic()
    # down 받은 파일을 불러오기
    current_dir = os.path.dirname(os.path.abspath(__file__))
    down_dir = os.path.join(current_dir, 'traffic_data')
    for file in os.listdir(down_dir):
        if file.endswith(".csv"):
            file_path = os.path.join(down_dir, file)
            print(file_path)
            print("="*100)
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                  pattern_time = "[0-2][0-9]:[0-5][0-9]:[0-5][0-9]"
                  if re.finditer(pattern_time, line) is None:
                    continue

                  data = line.strip().split(',')
                  if data[2] == "LINUX" or len(data[2]) == 0 or data[3].endswith("Average:"):
                    continue
                  hostname = data[0]
                  ip_address = data[1]
                  interface_name = data[2]
                  date_time = data[3]
                  rxkB_per_second = data[4]
                  txkB_per_second = data[5]
                  print("all data ============", hostname, ip_address, interface_name, date_time, rxkB_per_second, txkB_per_second, "-------------")
                  # hostinfo = db.session.query(HostInfos).filter_by(ip_address=ip_address).first()

    return "<h1>SAR TRAFFIC 생성 완료</h1>"
    # hostinfos = get_host_info()
    # for info in hostinfos:
    #     query_existing = db.session.query(HostInfos)\
    #         .filter_by(ip_address=info.get("ip_address")).first()
    #     if query_existing:
    #         continue
    #     new_host = HostInfos(
    #         hostname=info.get("hostname"), 
    #         ip_address=info.get("ip_address"))
    #     db.session.add(new_host)
    #     server = db.session.query(Servers).filter_by(ip_address=info.get("ip_address")).first()
    #     if server:
    #         new_host.access_info = server
    #     db.session.commit()
    # return redirect(url_for("hostinfos.index"))

# @bp.route("/")
# def index():
#     hostinfos = db.session.query(HostInfos).all()
#     current_user_id = current_user.get_id()
#     # hostinfo를 통해 사용자 id로 필터링
#     hostinfo_server_by_user = db.session.query(HostInfos)\
#         .join(HostInfos.access_info)\
#         .join(Servers.operators)\
#         .filter(Users.id == current_user_id).all()

#     return render("health/hostinfos/hostinfos_home.html", 
#         hostinfo_server_by_user=hostinfo_server_by_user, 
#         hostinfos=hostinfos)
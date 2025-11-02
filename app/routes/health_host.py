from flask import (
  Blueprint, request, redirect, 
  render_template as render, flash, url_for) # type: ignore
from flask_login import current_user, login_required
from ..extensions import db
from ..models.users import Users
from ..models.servers import Servers
from ..models.get_host import HostInfos
from .pagenation import pagenation

bp = Blueprint("hostinfos", __name__, url_prefix="/health/hostinfos")

@bp.route("/")
def index():
    hostinfos = db.session.query(HostInfos).all()
    pagination_data = pagenation(HostInfos)
    current_user_id = current_user.get_id()
    hostinfo_server_by_user = db.session.query(HostInfos)\
        .join(HostInfos.access_info)\
        .join(Servers.operators)\
        .filter(Users.id == current_user_id).all()

    return render("health/hostinfos/hostinfos_home.html", 
        hostinfo_server_by_user=hostinfo_server_by_user, 
        hostinfos=hostinfos,
        servers=pagination_data['query_result'], 
        page=pagination_data['page'], 
        per_page=pagination_data['per_page'], 
        start_page=pagination_data['start_page'], 
        end_page=pagination_data['end_page'], 
        total_pages=pagination_data['total_pages'], 
		page_len=pagination_data['page_len'])

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_host():
    users = db.session.query(Users).all()
    if request.method == "POST":
        hostname = request.form.get("hostname")
        ip_address = request.form.get("ip_address")

        if not ip_address or not hostname:
            flash("IP 주소, hostname은 필수입니다.")
            return render(url_for("hostinfos.create_host"))
        query_access_info = db.session.query(Servers).filter_by(ip_addr=ip_address).first()
        if not query_access_info:
            flash("현결 가능한 서버가 없습니다. 서버를 먼저 생성해주세요.")
            return render(url_for("hostinfos.create_host"))

        new_host = HostInfos(hostname=hostname, ip_address=ip_address)

        access_info_id = request.form.getlist("access_info")
        if access_info_id:
            server = db.session.query(Servers).get(access_info_id)
            new_host.access_info = server

        db.session.add(new_host)
        db.session.commit()
        flash(f"Hostname '{new_host.hostname}' created successfully.")
        return redirect(url_for("hostinfos.index"))
    return render("health/hostinfos/create_hostinfo.html", users=users)

@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_host(id):
    host = db.session.query(HostInfos).filter_by(id=id).first_or_404()
    users = db.session.query(Users).all()

    if request.method == "POST":
        hostname = request.form.get("hostname")
        ip_address = request.form.get("ip_address")

        if not ip_address or not hostname:
            flash("IP 주소, hostname은 필수입니다.")
            return render(url_for("hostinfos.edit_host", id=id))

        host.hostname = hostname
        host.ip_address = ip_address

        access_info_id = request.form.getlist("access_info")
        if access_info_id:
            server = db.session.query(Servers).get(access_info_id)
            host.access_info = server

        db.session.commit()
        flash(f"Host '{host.hostname}' updated successfully.")
        return redirect(url_for("hostinfos.index"))

    return render("health/hostinfos/edit_hostinfo.html", users=users, host=host)

@bp.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_host(id):
    host = db.session.query(HostInfos).filter_by(id=id).first()
    if request.method == "POST":
        db.session.delete(host)
        db.session.commit()
        return redirect(url_for("hostinfos.index"))
    else:
        return render("health/hostinfos/delete_hostinfo.html", host=host)

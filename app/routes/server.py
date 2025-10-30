from flask import (
  Blueprint, request, redirect, 
  render_template as render, flash, url_for) # type: ignore
from flask_login import login_required, current_user
from ..extensions import db
from ..models_server import SV_SSH as Server, Users
from .pagenation import pagenation

bp = Blueprint("server_list", __name__, url_prefix="/servers")

@bp.route("/")
def server_home():
    pagination_data = pagenation(Server)
    return render("server/server_home.html", 
        servers=pagination_data['query_result'], 
        page=pagination_data['page'], 
        per_page=pagination_data['per_page'], 
        start_page=pagination_data['start_page'], 
        end_page=pagination_data['end_page'], 
        total_pages=pagination_data['total_pages'], 
		page_len=pagination_data['page_len'])

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_server():
    users = db.session.query(Users).all()
    if request.method == "POST":
        server_name = request.form.get("server_name")
        server_ip = request.form.get("server_ip")
        username = request.form.get("username")
        password = request.form.get("password")

        if not server_ip or not server_name:
            flash("서버 이름과 서버 주소는 필수입니다.")
            return render("server/create_server.html", users=users)
        
        new_server = Server(server_name=server_name, server_ip=server_ip, username=username)
        new_server.set_password(password)

        # Get operator IDs from the form and fetch user objects
        operator_ids = request.form.getlist("operators")
        if operator_ids:
            operators = db.session.query(Users).filter(Users.id.in_(operator_ids)).all()
            new_server.operators = operators

        db.session.add(new_server)
        db.session.commit()
        flash(f"Server '{server_name}' created successfully.")
        return redirect(url_for("server_list.server_home"))
    return render("server/create_server.html", users=users)

@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_server(id):
    server = db.session.query(Server).filter_by(id=id).first_or_404()
    users = db.session.query(Users).all()

    if request.method == "POST":
        server_name = request.form["server_name"]
        server_ip = request.form["server_ip"]
        username = request.form["username"]
        password = request.form["password"]
        
        if not server_name or not server_ip:
            flash("서버 이름과 서버 주소는 필수입니다.")
            return render("server/edit_server.html", server=server, users=users)
        
        server.server_name = server_name
        server.server_ip = server_ip
        server.username = username
        if password:
            server.set_password(password)

        operator_ids = request.form.getlist("operators")
        operators = db.session.query(Users).filter(Users.id.in_(operator_ids)).all()
        server.operators = operators

        db.session.commit()
        flash(f"Server '{server.server_name}' updated successfully.")
        return redirect(url_for("server_list.server_home"))
    
    return render("server/edit_server.html", server=server, users=users)

@bp.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_server(id):
    if request.method == "POST":
        server = db.session.query(Server).filter_by(id=id).first()
        db.session.delete(server)
        db.session.commit()
        return redirect(url_for("server_list.server_home"))
    elif request.method == "GET":
        server = db.session.query(Server).filter_by(id=id).first()
        return render("server/delete_server.html", server=server)
    return None

from flask import (Blueprint, redirect, render_template as render, flash, url_for) # type: ignore
from flask_login import login_required, current_user
from ..extensions import db
from ..models_server import SV_SSH as Server
from .pagenation import pagenation
from ..server_info.get_server_info import get_server_info

bp = Blueprint("health_check", __name__, url_prefix="/health")

@bp.route("/server_infos")
@login_required
def server_infos():
    server_list = db.session.query(Server).all()
    health_results = []

    if not server_list:
        flash("No servers found in the database.")
        return redirect(url_for("server_list.server_home"))
    else:
        for server in server_list:
            health_results.append(get_server_info(server))
    # pagination_data = pagenation(Blog)
    flash(f"Get server informations success({len(server_list)} servers) !.")
    return render("health/health_check_result.html", health_results=health_results, count_server=len(server_list))


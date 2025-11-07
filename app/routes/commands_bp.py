from flask import (Blueprint, request, render_template as render, 
    redirect, flash, url_for )
from flask_login import login_required # type: ignore
from sqlalchemy import or_ # type: ignore
from ..extensions import db
from ..models.commands import Commands, CAT
from .pagenation import pagenation

bp = Blueprint('commands', __name__, url_prefix='/health/commands')

@bp.route('/')
def index_cmds():
    search_name = request.args.get('search_name', '')
    search_cmd = request.args.get('search_cmd', '')
    selected_category = request.args.get('category', '')

    query = db.session.query(Commands)

    filters = []
    if search_name:
        filters.append(Commands.name.ilike(f'%{search_name}%'))
    if search_cmd:
        filters.append(Commands.cmd.ilike(f'%{search_cmd}%'))
    if selected_category:
        filters.append(Commands.category == selected_category)
    
    if filters:
        query = query.filter(or_(*filters))

    pg_data = pagenation(query=query, per_page=10, orders=Commands.category.asc())

    categories = [cat.value for cat in CAT]

    return render('health/commands/cmd_home.html', 
        categories=categories,
        cmd_list=pg_data['query_result'], 
        pagination=pg_data,
        search_name=search_name,
        search_cmd=search_cmd)

@bp.route('/create', methods=['GET','POST'])
def create_cmd():
    if request.method == 'POST':
        category = request.form.get("category")
        name = request.form.get("name")
        cmd = request.form.get("cmd")
        if category is None or name is None or cmd is None:
            flash('모든 필드를 채워주세요.', category='alert')
            return render('health/commands/create_cmd.html', categories=[cat.value for cat in CAT])
 
        # Check if a command with the same name OR cmd text already exists.
        existing_cmd = Commands.query.filter(or_(Commands.name == name, Commands.cmd == cmd)).first()
        if existing_cmd:
            flash(f'A command with the same name or command already exists.')
            return render('health/commands/create_cmd.html', categories=[cat.value for cat in CAT])
        
        else:
            new_cmd = Commands(category=category, name=name, cmd=cmd)
            db.session.add(new_cmd)
            db.session.commit()
 
            flash('명령어가 추가되었습니다.!', category='success')
            return redirect(url_for('commands.index_cmds'))
    return render('health/commands/create_cmd.html', 
                  categories=[cat.value for cat in CAT])

@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_cmd(id):
    current_cmd = db.session.get(Commands, id)
    if not current_cmd:
        flash("해당 명령어가 없습니다.", category="alert")
        return redirect(url_for("commands.index_cmds")), 404
    if request.method == "POST":
        category = request.form.get("category")
        desc = request.form.get("name")
        cmd = request.form.get("cmd")

        # Check if either name or cmd has changed
        if current_cmd.name != desc or current_cmd.cmd != cmd:
            existing_cmd = Commands.query.filter(or_(Commands.name == desc, Commands.cmd == cmd)).first()
            if existing_cmd:
                flash(f'A command with the same name or command already exists.', category="alert")
                return render('health/commands/edit_cmd.html', cmd=current_cmd, 
                              categories=[cat.value for cat in CAT])

        current_cmd.category = category
        current_cmd.name = desc
        current_cmd.cmd = cmd

        db.session.commit()

        flash("명령어가 수정되었습니다.")
        return redirect(url_for("commands.index_cmds"))
    return render("health/commands/edit_cmd.html", cmd=current_cmd, 
                  categories=[cat.value for cat in CAT])

@bp.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_cmd(id):
    cmd = db.session.query(Commands).get(id)
    if request.method == "POST":
        if cmd is None:
            flash("해당 명령어가 없습니다.", category="alert")
            return redirect(url_for("commands.index_cmds"))
        db.session.delete(cmd)
        db.session.commit()
        flash("명령어가 삭제되었습니다.", category="success")
        return redirect(url_for("commands.index_cmds"))
    return render("health/commands/delete_cmd.html", cmd=cmd)
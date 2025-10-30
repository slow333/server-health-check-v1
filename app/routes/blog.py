from flask import (
  Blueprint, request, redirect, 
  render_template as render, flash, url_for) # type: ignore
from flask_login import login_required, current_user
from ..extensions import db
from ..models_blog import Blog
from .pagenation import pagenation

bp = Blueprint("blog_content", __name__, url_prefix="/blogs")

@bp.route("/")
def blog_home():
    pagination_data = pagenation(Blog)
    return render("blog/blog_home.html", 
        blogs=pagination_data['query_result'], 
        page=pagination_data['page'], 
        per_page=pagination_data['per_page'], 
        start_page=pagination_data['start_page'], 
        end_page=pagination_data['end_page'], 
        total_pages=pagination_data['total_pages'], 
		page_len=pagination_data['page_len'])

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_blog():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        comment = request.form["comment"]

        if not title or not content:
            flash("타이틀과 컨텐트는 필수입니다.")
            return render("blog/create_blog.html")
        else:
            db.session.add(Blog(title=title, content=content, comment=comment, author_id=current_user.id))
        db.session.commit()
        return redirect(url_for("blog_content.blog_home"))
    return render("blog/create_blog.html")

@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_blog(id):
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        comment = request.form["comment"]
        
        if not title or not content:
            flash("타이틀과 컨텐트는 필수입니다.")
            return render("blog/update_blog.html")
        else:
            blog = db.session.query(Blog).filter_by(id=id).first()
            blog.title = title
            blog.content = content
            blog.comment = comment
            db.session.commit()
            return redirect(url_for("blog_content.blog_home"))
    else:
        blog = db.session.query(Blog).filter_by(id=id).first()
        return render("blog/edit_blog.html", blog=blog)

@bp.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_blog(id):
    if request.method == "POST":
        blog = db.session.query(Blog).filter_by(id=id).first()
        db.session.delete(blog)
        db.session.commit()
        return redirect(url_for("blog_content.blog_home"))
    elif request.method == "GET":
        blog = db.session.query(Blog).filter_by(id=id).first()
        return render("blog/delete_blog.html", blog=blog)
    return None

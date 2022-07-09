import os
from flask import render_template, request, flash, url_for
from app import db
from app.dashboard import bp
from app.models import Post, PostLikes
from flask_login import login_required, current_user
from app.dashboard.forms import PostingForm
from werkzeug.utils import secure_filename, redirect


@bp.route('/', methods=["GET", "POST"])
@login_required
def index():
    form = PostingForm()
    posts = Post.query.filter_by(user_id=current_user.get_id()).all()
    if form.validate_on_submit():
        file = request.files['file']
        file_name = secure_filename(file.filename)
        user_id = current_user.get_id()
        path = os.path.join('static/images', current_user.get_id())
        if not os.path.exists(path):
            os.makedirs(path)
        file_path = os.path.join(path, file_name)
        post = Post(user_id=user_id, title=form.title.data, description=form.description.data, file_path=file_path)
        db.session.add(post)
        db.session.commit()
        file.save(file_path)
        flash("You have successfully added a post!")
        return redirect(url_for('dashboard.index'))
    return render_template('dashboard/index.html', form=form, posts=posts)


@bp.route('/explore', methods=["GET", "POST"])
@login_required
def explore():
    posts = Post.query.filter(Post.user_id != current_user.id).all()
    return render_template('dashboard/explore.html', posts=posts)


@bp.route('/posts/remove/<int:id>')
@login_required
def remove_post(id: int):
    post = Post.query.filter_by(id=id).first()
    PostLikes.query.filter_by(post_id=id).delete()
    if post is not None:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('dashboard.index'))


@bp.route('/posts/like/<int:id>')
@login_required
def like_post(id: int):
    post = Post.query.filter_by(id=id).first()
    if post is not None:
        post_like = PostLikes(post_id=post.id, user_id=current_user.get_id())
        db.session.add(post_like)
        db.session.commit()
    return redirect(url_for('dashboard.explore'))


@bp.route('/posts/dislike/<int:id>')
@login_required
def dislike_post(id: int):
    post_like = PostLikes.query.filter_by(post_id=id, user_id=current_user.get_id()).first()
    if post_like is not None:
        db.session.delete(post_like)
        db.session.commit()
    return redirect(url_for('dashboard.explore'))

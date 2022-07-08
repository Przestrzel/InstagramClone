import os
from flask import render_template, request
from app import db
from app.dashboard import bp
from app.models import Post
from flask_login import login_required, current_user
from app.dashboard.forms import PostingForm
from werkzeug.utils import secure_filename


@bp.route('/', methods=["GET", "POST"])
@login_required
def index():
    form = PostingForm()
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

    return render_template('dashboard/index.html', form=form)


@bp.route('/explore', methods=["GET", "POST"])
@login_required
def explore():
    return render_template('dashboard/explore.html')

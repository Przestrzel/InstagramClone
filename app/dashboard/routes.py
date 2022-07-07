from flask import render_template, redirect, url_for
from flask_login import current_user
from app.dashboard import bp
from flask_login import login_required


@bp.route('/', methods=["GET", "POST"])
@login_required
def index():
    return render_template('dashboard/index.html')

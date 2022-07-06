from flask import render_template

from app.dashboard import bp
from flask_login import login_required


@bp.route('/', methods=["GET", "POST"])
@login_required
def index():
    return render_template('dashboard/index.html')

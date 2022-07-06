from flask import render_template
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form)

    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form)

    return render_template('auth/register.html', form=form)

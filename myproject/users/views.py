from flask import Flask, render_template, Blueprint, redirect, flash, url_for, request, session
from flask_login import login_user, current_user, logout_user, login_required
from myproject import db
from myproject.models import User, Project
from myproject.users.forms import RegistrationForm,LoginForm
import time
import os

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,last_name=form.last_name.data,
                    email=form.email.data,phone_no=form.phone_no.data,company_name=form.company_name.data,
                    username=form.username.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()

        time.sleep(2)

        dir_name = str(user.id)+'_'+user.username
        main_database = './user_profiles'

        path = os.path.join(main_database, dir_name)
        os.mkdir(path)

        flash('Thanks for registration!')
        # return redirect(url_for('users.dashboard'))
        return redirect(url_for('users.login'))

    # Repeat handling

    elif User.query.filter_by(email=form.email.data).first() and User.query.filter_by(username=form.username.data).first():
        flash('The email and username already exists.')

    elif User.query.filter_by(email=form.email.data).first():
        flash('This email already exists.')

    elif User.query.filter_by(username=form.username.data).first():
        flash('This username already exists.')

    elif form.password.data != form.pass_confirm.data:
        flash('Your passwords do not match. Please re-confirm the passwords.')

    return render_template('register.html',form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('Please enter a valid email.')

        elif user.check_password(form.password.data) == False:
            flash('Incorrect Password.')

        elif user.check_password(form.password.data) and user is not None:
            username = user.username
            login_user(user)

            flash('Log in Success!')
            #return render_template('dashboard.html', form=form, username=username)
            return redirect(url_for('users.dashboard'))
            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html',form=form)

@users.route('/dashboard')
@login_required
def dashboard():
    username = current_user.username
    company = current_user.company_name
    email = current_user.email
    phone_no = current_user.phone_no

    return render_template('dashboard.html', username=username, company=company, email=email, phone_no=phone_no)

@users.route('/view_projects')
@login_required
def old_projects():
    page = request.args.get('page', 1, type=int)
    projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.date.desc()).paginate(page=page, per_page=5)

    return render_template('view_projects.html', projects=projects)
    
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))
from flask import render_template, url_for, flash, redirect, request
from songfinder import app, db
from songfinder.forms import RegisterForm, LoginForm
from songfinder.models import User, Aid
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


songs = [
    {
        'artist': 'Pearl Jam',
        'title': 'Yellow Ledbetter',
        'hits': 88,
        'date_posted': 'April 20, 2019'
    },
    {
        'artist': 'Radiohead',
        'title': 'Paranoid Android',
        'hits': 86,
        'date_posted': 'April 22, 2019'
    }
]

@app.route('/')
def home():
    return render_template('home.html', songs=songs)

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() 
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = 'home'
        return redirect(url_for(next_page))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
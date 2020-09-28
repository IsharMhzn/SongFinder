from songfinder import app, db
from songfinder.forms import RegisterForm, LoginForm, AidForm
from songfinder.models import User, Aid, Spotify
from songfinder.spotify_client import get_bearer_token, authorize_account

from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

import os, requests, json, threading

@app.route('/', methods=['GET', 'POST'])
def home():
    aids = Aid.query.all()
    print(aids)
    if current_user.is_authenticated:
        form = AidForm()
        if form.validate_on_submit():
            # TODO: to save the genre
            userid = current_user.id
            aid = Aid(title=form.title.data.lower(), artist=form.artist.data.lower(), album=form.album.data.lower(), story=form.story.data.lower(), userid=userid)
            db.session.add(aid)
            db.session.commit()
            flash('Your aid has been posted safe and sound.')
            return redirect(url_for('home'))
        return render_template('home.html', aids=aids, form=form)
    return render_template('home.html', aids=aids)

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
        if next_page := request.args.get('next'):
            next_page = next_page[1:]
        elif not next_page or url_parse(next_page).netloc != '':
            next_page = 'home'
        return redirect(url_for(next_page))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    aids = Aid.query.filter_by(userid=user.id)
    if spotc := Spotify.query.filter_by(userid=user.id).first():
        spotc = True
    else:
        spotc = False if user==User.query.filter_by(id=current_user.id).first_or_404() else True
    return render_template('profile.html', user=user, aids=aids, spotc=spotc)

@app.route('/search', methods=['GET'])
def search():
    search = request.args.get('q-search')
    aids_t = Aid.query.filter_by(title=search)
    aids_g = Aid.query.filter_by(genre=search)
    aids_a = Aid.query.filter_by(artist=search)
    return render_template('result.html', aids_t=aids_t, aids_g=aids_g, aids_a=aids_a)

@app.route('/similar/<artist>')
def similar(artist):
    url_search = f"https://api.spotify.com/v1/search?q={artist}&type=artist"
    auth_token = get_bearer_token()
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.request("GET", url=url_search, headers=headers).text.encode("utf-8")
    resp = json.loads(response)
    entity = resp.get("artists").get("items")[0]
    if not entity:
        return "Sorry the server's having some technical problems. Please check later."
    artistid = entity.get('id')
    url_artists = f"https://api.spotify.com/v1/artists/{artistid}/related-artists"
    response = requests.request("GET", url=url_artists, headers=headers).text.encode("utf-8")
    resp = json.loads(response)
    return render_template('artist.html', **entity, **resp)

@app.route('/spotify/authorize/')
def connect_spotify():
    if code:=request.args.get('code'):
        userid = current_user.id
        if not Spotify.query.filter_by(userid=userid).first():
            s = Spotify(userid=userid, code=code)
            db.session.add(s)
            db.session.commit()
        else:
            flash('You are already connected to spotify')
        return redirect(url_for('home'))
    url = authorize_account()
    return redirect(url)
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '138cf4922332d7a0e98fc4ac6067238b2273f336'

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
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): 
        if form.email.data == "ishar@ishar.com" and form.password.data=="ishar":
            flash(f'Account created for {form.email.data}', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Incorrect email or password.')
    return render_template('login.html', form=form)

if __name__=="__main__":
    app.run(debug=True)
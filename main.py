from flask import Flask, render_template, url_for

app = Flask(__name__)

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

if __name__=="__main__":
    app.run(debug=True)
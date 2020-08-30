from songfinder import app, db
from songfinder.models import User, Aid

#flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Aid': Aid}

if __name__=="__main__":
    app.run(debug=True)
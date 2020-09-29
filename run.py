from songfinder import socketapp, db, app
from songfinder.models import User, Aid

#flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Aid': Aid}

if __name__=="__main__":
    socketapp.run(app)
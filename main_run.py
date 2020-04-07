'''The main file in the project for running Flask app'''

from app import app, db
from app.models import User, Questions, Answers

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Questions': Questions, 'Answers': Answers}

if __name__ == '__main__':
    app.run(debug=True)

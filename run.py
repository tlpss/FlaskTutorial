from server import app,db
from server.models import User,Post

# allows to access all variables declared in dict from the bash command 'flaks shell'
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
##

if __name__ == "__main__":
    app.run(debug = True)
from flask import render_template
from server import app, db


# second arg of return : error code, default = 200
@app.errorhandler(404) # not found
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500) # db error
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
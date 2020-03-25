from app import app

@app.route('/')
@app.route('/index')
def index():
    return 'TODO: this file will be used in the actual application'
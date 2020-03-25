from app import app
from flask import send_from_directory
from flask import make_response, render_template, request
from flask import url_for, redirect

@app.route('/')
@app.route('/login')
# Home page with login screen. Should be different if logged in, this is just the login screen as of now
def homepage():
    html = render_template('homepage.html',
        title='Home | Spot')
    response = make_response(html)
    return response
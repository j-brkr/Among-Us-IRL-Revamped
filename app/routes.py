from flask import flash, render_template, redirect, url_for, request
from app import app
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for("select_user"))

@app.route('/select_user')
def select_user():
    '''
    User selection page
    '''
    users = db.session.scalars(sa.select(User)).all()
    return render_template("select_user.html", title="Select User", users=users)

# GET request
@app.get('/sign_in/<username>')
def sign_in(username):
    '''
    Sign in page
    '''
    # Redirect if already signed in
    if current_user.is_authenticated:
        return redirect(url_for('game'))
    
    # Find user object and check it exists
    user = db.session.scalar( 
        sa.select(User).where(User.name == username))
    if user is None:
        flash('Invalid user')
        return redirect(url_for('select_user'))
    
    return render_template("sign_in.html", title="Sign In", user=user)

@app.post('/sign_in/<username>')
def sign_in_post(username):
    '''
    Handles POST requests to sign_in. 
    This runs when the PIN is submitted
    '''
    # Find user object and check it exists
    user = db.session.scalar( 
        sa.select(User).where(User.name == username))
    if user is None:
        flash('Invalid user')
        return redirect(url_for('select_user'))
    # Get the pin and check it is correct
    key, value = request.get_data(as_text=True).split("=")
    if not user.check_pin(value):
        flash('Incorrect PIN')
        return redirect(url_for('sign_in', username=username))
    login_user(user, remember=True)
    return redirect(url_for('game'))

@app.route('/game')
def game():
    '''
    The webpage once logged in.
    Used for the lobby and when the game is being played
    '''
    return "Game page"
        

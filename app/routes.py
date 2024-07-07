from flask import flash, render_template, redirect, url_for, request
from app import app
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db, interfaces
from app.models import User, Game
from app.forms import settingsForm

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for("select_user"))

@app.route('/select_user')
def select_user():
    '''
    User selection page
    '''
    # Log out if already signed in
    if current_user.is_authenticated:
        logout_user()
    
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

@app.route('/player')
@login_required
def player():
    '''
    The webpage for users once logged in.
    Used for the lobby and when the game is being played
    '''
    return "Player Game page"

# Gamemaster

@app.route('/directories')
def directories():
    '''
    A directory page
    Shows directories for different machines and interfaces
    '''
    return render_template("directories.html")

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    '''
    Settings page
    Adjust settings and start games
    '''
    form = settingsForm()
    if form.validate_on_submit():
        # Check no running game
        active_game = db.session.scalar(sa.select(Game).where(Game.active))
        if active_game is not None:
            print("GAME "+active_game+" already running!")
            flash("Game in progress")
            return redirect(url_for('settings'))
        
        # Make new game object
        game = Game(
            active=True,
            status="LOBBY",
            imposter_count=form.imposter_count.data,
            reveal_role=form.reveal_role.data,
            emergency_meetings=form.emergency_meetings.data,
            discussion_time=form.discussion_time.data,
            emergency_cooldown=form.emergency_cooldown.data,
            kill_cooldown=form.kill_cooldown.data,
            short_tasks=form.short_tasks.data,
            long_tasks=form.long_tasks.data,
            common_tasks=form.common_tasks.data
        )
        db.session.add(game)
        db.session.commit()
        
        return redirect(url_for('central'))
    return render_template("settings.html", form=form)

# Central

@app.route('/central')
def central():
    '''
    Games page for Central.
    Shows emergency meeting button, voting screen and winner
    '''
    return render_template("central.html")

# Interfaces

@app.route('/interfaces/<path:path>')
def interface_route(path):
    if path in interfaces.route.keys():
        return interfaces.route[path]()
    return "Interface " + path + " does not exists"

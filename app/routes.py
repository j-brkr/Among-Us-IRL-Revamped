from flask import flash, render_template, redirect, url_for, request
from app import app
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db, interfaces
from app.models import User, Game, Player, Room, PlayerTask, Task
from app.forms import settingsForm

import json

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
        return redirect(url_for('player'))
    
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
    
    # Get current game
    active_game = Game.get_active_game()
    if active_game is None:
        flash('No active game')
        return redirect(url_for('sign_in', username=username))
    
    login_user(user, remember=True)

    return redirect(url_for('player'))

@app.route('/player')
@login_required
def player():
    '''
    The webpage for users once logged in.
    Used for the lobby and when the game is being played
    '''
    
    # Get current game
    active_game = Game.get_active_game()
    if active_game is None:
        return "No active game. Wait for settings to be submitted, then refresh the page"
    
    # Create a player if not already existant
    player = active_game.player_of_user(current_user)
    if player is None:
        player = Player(game_id = active_game.id, user_id = current_user.id)
        db.session.add(player)
        db.session.commit()

    tasks = db.session.scalars(sa.select(PlayerTask).where(PlayerTask.player_id==player.id)).all()
    return render_template("player.html", title="Player", user=current_user, player=player, tasks=tasks)

@app.route('/role-reveal')
@login_required
def role_reveal():
    # Get current game
    game = Game.get_active_game()
    if game is None: return "No active game", 404
    
    # Get player
    player = game.player_of_user(current_user)

    imposters = []

    return render_template("role-reveal.html", imposters=imposters)

@app.route('/player-task_box')
@login_required
def task_box():
    # Get current game
    game = Game.get_active_game()
    if game is None: return "No active game", 404
    
    # Get player
    player = game.player_of_user(current_user)

    tasks = db.session.scalars(sa.select(PlayerTask).where(PlayerTask.player_id==player.id)).all()
    return render_template("player-task_box.html", player=player, tasks=tasks)

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
        active_game = Game.get_active_game()
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
    game = Game.get_active_game()
    if game is None:
        flash("No game running")
        return redirect(url_for('directories'))
    players = db.session.scalars(sa.select(Player).where(Player.game_id==game.id)).all()
    return render_template("central.html", players = players)

# Interfaces

@app.route('/interfaces/<path:path>')
def interface_route(path):
    if path in interfaces.route.keys():
        return interfaces.route[path]()
    return "Interface " + path + " does not exists"

# Game API

@app.route("/api/<path:path>", methods=['GET', 'POST', 'PUT'])
def api(path):
    path_parts = path.split("/")
    resource = path_parts[0]
    # relates to current game
    if resource=="game":
        # Get the current game and return 404 on failure
        active_game = Game.get_active_game()
        if active_game is None: 
            return url_for("settings")

        if len(path_parts) == 1:
            # Game object
            response = active_game.as_dict()
            return response
        elif path_parts[1] == "players":
            # Player array
            players = db.session.scalars(active_game.players.select()).all()
            response = [player.as_dict() for player in players]
            return response
        elif path_parts[1] == "imposter_count":
            response = {"imposter_count": active_game.imposters_alive()}
            return response
    elif resource=="player":
        id = int(path_parts[1])
        player = Player.query.get(id)
        if player is None: return "{} {} not found".format(resource, id), 404
        if request.method == 'PUT':
            p = request.get_json()
            player.alive = p["alive"]
            db.session.add(player)
            db.session.commit()
        return player.as_dict()
    elif resource=="player_task":
        id = int(path_parts[1])
        ptask = db.session.scalar(sa.select(PlayerTask).where(PlayerTask.id==id))
        if ptask is None: return "{} {} not found".format(resource, id), 404
        if request.method=='PUT':
            p = request.get_json()
            ptask.completed = p["completed"]
            db.session.add(ptask)
        db.session.commit()
        return "success"
    return "The resource {} could not be found".format(path), 404

@app.route("/command/<string:command_string>", methods=['GET', 'POST', 'PUT'])
def command(command_string):
    game = Game.get_active_game()
    if command_string=="START_GAME":
        if game.status != "LOBBY":
            return ("Cannot start game, this game is in status: " + game.status), 403

        game.assign_roles()
        game.assign_tasks()
        game.status = "REVEAL"
        db.session.commit()
        return "Role Reveal!", 200
    elif command_string=="END_REVEAL":
        if game.status != "REVEAL":
            return ("Cannot end role reveal, this game is in status: " + game.status), 403
        game.start_game()
        return "Game Started!", 200
    elif command_string=="EMERGENCY":
        if game.status != "GAME":
            return ("Cannot call emergency meeting, this game is in status: " + game.status), 403
        game.emergency()
        return "Emergency Called!", 200
    elif command_string == "EJECTED":
        if game.status != "MEETING":
            return ("Cannot end emergency meeting, this game is in status: " + game.status), 403
        game.status = "GAME"
        db.session.commit()
        return "Game resuming!", 200

    return "Unrecognized command: " + str(command_string), 404


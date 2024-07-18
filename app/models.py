from datetime import datetime, timezone
import json
import os
import random
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from app import db, login

def load_datapack(path):
    Room.load(path)
    Task.load(path)
    User.load(path)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32))
    color: so.Mapped[str] = so.mapped_column(sa.String(7))
    pin: so.Mapped[str] = so.mapped_column(sa.String(6))

    players: so.WriteOnlyMapped['Player'] = so.relationship(back_populates='user')

    def load(data_path):
        db.session.query(User).delete()
        user_path = os.path.join(data_path, "users.json")
        try:
            with open(user_path, 'r') as file:
                data = json.load(file)
                for user_data in data:
                    db.session.add(User(name=user_data["name"], color=user_data["color"], pin=user_data["pin"]))
                db.session.commit()

        except FileNotFoundError:
            print("Error loading User file " + user_path + " . The file does not exist")

    def check_pin(self, pin):
        return self.pin == pin
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return "<User {}>".format(self.name)
    
class Game(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    active: so.Mapped[bool]
    status: so.Mapped[str] = so.mapped_column(sa.String(32))
    time_started: so.Mapped[int] = so.mapped_column(sa.Integer(), default=0)
    time_finished: so.Mapped[int] = so.mapped_column(sa.Integer(), default=0)

    imposter_count: so.Mapped[int]
    reveal_role: so.Mapped[bool]
    emergency_meetings: so.Mapped[int]
    discussion_time: so.Mapped[int]
    emergency_cooldown: so.Mapped[int]
    kill_cooldown: so.Mapped[int]
    short_tasks: so.Mapped[int]
    long_tasks: so.Mapped[int]
    common_tasks: so.Mapped[int]

    players: so.WriteOnlyMapped['Player'] = so.relationship(back_populates='game')

    def check_win(self):
        if self.imposters_alive() < 1:
            self.status = "CREW_WIN"
            self.time_finished = datetime.now(timezone.utc)
            db.session.commit()
        
        if self.imposters_alive() >= self.crew_alive():
            self.status = "IMPOSTER_WIN"
            self.time_finished = datetime.now(timezone.utc)
            db.session.commit()

    def get_active_game():
        return db.session.scalar(sa.select(Game).where(Game.active))
    
    def assign_roles(self):
        players = db.session.scalars(sa.select(Player).where(Player.game_id == self.id)).all()
        crew_count = len(players) - self.imposter_count
        roles = [0] * crew_count + [1] * self.imposter_count
        random.shuffle(roles)
        for i, player in enumerate(players):
            player.role = roles[i]
            print("{} has role: {}".format(player.user.name, player.role))
    

    def assign_tasks(self):
        short_tasks = db.session.scalars(sa.select(Task).where(Task.type=="S")).all()
        long_tasks = db.session.scalars(sa.select(Task).where(Task.type=="L")).all()
        common_tasks = db.session.scalars(sa.select(Task).where(Task.type=="C")).all()
        chosen_common_tasks = random.sample(common_tasks, self.common_tasks)
        players = db.session.scalars(sa.select(Player).where(Player.game_id == self.id)).all()
        for player in players:
            tasks = random.sample(short_tasks, self.short_tasks) + random.sample(long_tasks, self.long_tasks) + chosen_common_tasks
            for task in tasks:
                db.session.add(PlayerTask(player_id=player.id, task_id = task.id))
                print("Adding task " + task.name + " to " + player.user.name + "'s list")
        db.session.commit()
    
    def start_game(self):
        self.status = "GAME"
        self.time_started = datetime.now(timezone.utc)
        db.session.commit()

    def emergency(self):
        self.status = "MEETING"
        db.session.commit()
    
    def get_imposters(self):
        players = db.session.scalars(sa.select(Player).where(Player.game_id==self.id)).all()
        imposters = [(1 if player.role==1 else 0) for player in players if player.alive]
        return imposters
    
    def imposters_alive(self):
        players = db.session.scalars(sa.select(Player).where(Player.game_id==self.id)).all()
        count = sum([(1 if player.role==1 else 0) for player in players if player.alive])
        return count
    
    def crew_alive(self):
        players = db.session.scalars(sa.select(Player).where(Player.game_id==self.id)).all()
        count = sum([(1 if player.role==0 else 0) for player in players if player.alive])
        return count

    def player_of_user(self, user):
        player = db.session.scalar(sa.select(Player).where(sa.and_(Player.game_id == self.id, Player.user_id == user.id)))
        return player

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __str__(self):
        return "<Game {} {}>".format(self.id, ("Active" if self.active else "Inactive"))
    

class Player(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    alive: so.Mapped[bool] = so.mapped_column(default=True)
    role: so.Mapped[int] = so.mapped_column(default=-1)
    # NONE = -1, CREW = 0, IMPOSTER = 1
    cooldown: so.Mapped[int] = so.mapped_column(default=0)

    game_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Game.id), index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))

    game: so.Mapped[Game] = so.relationship(back_populates='players')
    user: so.Mapped[User] = so.relationship(back_populates='players')

    player_tasks: so.WriteOnlyMapped['PlayerTask'] = so.relationship(back_populates='player')

    def as_dict(self):
        user_dict = self.user.as_dict()
        player_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        player_dict['user'] = user_dict
        return player_dict

class Room(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32))

    tasks: so.WriteOnlyMapped['Task'] = so.relationship(back_populates='room')

    def load(data_path):
        db.session.query(Room).delete()
        room_path = os.path.join(data_path, "rooms.json")
        try:
            with open(room_path, 'r') as file:
                data = json.load(file)
                for room_data in data:
                    db.session.add(Room(name=room_data["name"]))
                db.session.commit()

        except FileNotFoundError:
            print("Error loading Room file " + room_path + " . The file does not exist")

    def __repr__(self) -> str:
        return "Room(name='{}')".format(self.name)


class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32))
    type: so.Mapped[str] = so.mapped_column(sa.String(16))
    # SHORT, LONG, COMMON

    room_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Room.id))
    
    room: so.Mapped[Room] = so.relationship(back_populates='tasks')

    player_tasks: so.WriteOnlyMapped['PlayerTask'] = so.relationship(back_populates='task')

    def load(data_path):
        db.session.query(Task).delete()
        tasks_path = os.path.join(data_path, "tasks.json")
        try:
            with open(tasks_path, 'r') as file:
                data = json.load(file)
                for task_data in data:
                    room = db.session.scalar(sa.select(Room).where(Room.name==task_data["room"]))
                    if room is None:
                        print("Error loading tasks: The room {} does not exist".format(task_data["room"]))
                        return None
                    db.session.add(Task(name=task_data["name"], type=task_data["type"], room_id = room.id))
                db.session.commit()

        except FileNotFoundError:
            print("Error loading Room file " + tasks_path + " . The file does not exist")

class PlayerTask(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    completed: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    player_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), index=True)
    task_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Task.id))
    prerequesite_id: so.Mapped[int | None] = so.mapped_column(sa.ForeignKey('player_task.id', name='fk_playerTask_prequesite_id'))

    player: so.Mapped[Player] = so.relationship(back_populates='player_tasks')
    task: so.Mapped[Task] = so.relationship(back_populates='player_tasks')
    prerequesite: so.Mapped['PlayerTask | None'] = so.relationship(remote_side=[id], back_populates='successors')

    successors: so.WriteOnlyMapped['PlayerTask | None'] = so.relationship(back_populates='prerequesite')

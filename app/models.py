import random
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from app import db, login

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32))
    color: so.Mapped[str] = so.mapped_column(sa.String(7))
    pin: so.Mapped[str] = so.mapped_column(sa.String(6))

    players: so.WriteOnlyMapped['Player'] = so.relationship(back_populates='user')

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

    def get_active_game():
        return db.session.scalar(sa.select(Game).where(Game.active))
    
    def assign_roles(self):
        crew_count = len(self.players) - self.imposter_count
        roles = [0] * crew_count + [1] * self.imposter_count
        random.shuffle(roles)
        for i, player in enumerate(self.players):
            player.role = roles[i]
            print("{} has role: {}".format(player.user.name, player.role))

    def assign_tasks(self):
        pass

    def player_of_user(self, user):
        player = db.session.scalar(sa.select(Player).where(sa.and_(Player.game_id == self.id, Player.user_id == user.id)))
        return player

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return "<Game {} {}>".format(self.id, ("Active" if self.active else ""))
    

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

    player_tasks: so.WriteOnlyMapped['PlayerTask'] = so.relationship(back_populates='players')

    def as_dict(self):
        user_dict = self.user.as_dict()
        player_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        player_dict['user'] = user_dict
        return player_dict

class Room(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32))

    tasks: so.WriteOnlyMapped['Task'] = so.relationship(back_populates='room')

class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32))
    type: so.Mapped[str] = so.mapped_column(sa.String(16))
    # SHORT, LONG, COMMON

    room_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Room.id))
    
    room: so.Mapped[Room] = so.relationship(back_populates='tasks')

    player_tasks: so.WriteOnlyMapped['PlayerTask'] = so.relationship(back_populates='task')

class PlayerTask(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    completed: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    player_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), index=True)
    task_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Task.id))
    prerequesite_id: so.Mapped[int | None] = so.mapped_column(sa.ForeignKey('player_task.id'))

    player: so.Mapped[Player] = so.relationship(back_populates='player_tasks')
    task: so.Mapped[Task] = so.relationship(back_populates='player_tasks')
    prerequesite: so.Mapped['PlayerTask | None'] = so.relationship(back_populates='successors')

    successors: so.WriteOnlyMapped['PlayerTask | None'] = so.relationship(back_populates='prerequesite')

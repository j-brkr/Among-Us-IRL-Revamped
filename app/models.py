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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return "<Game {} {}>".format(self.id, ("Active" if self.active else ""))

class Player(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    alive: so.Mapped[bool] = so.mapped_column(default=True)
    role: so.Mapped[int] = so.mapped_column(default=0)
    # NONE = 0, CREW = 1, IMPOSTER = -1
    cooldown: so.Mapped[int] = so.mapped_column(default=0)

    game_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Game.id), index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))

    game: so.Mapped[Game] = so.relationship(back_populates='players')
    user: so.Mapped[User] = so.relationship(back_populates='players')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



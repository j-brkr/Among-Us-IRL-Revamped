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

    def check_pin(self, pin):
        return self.pin == pin

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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return "<Game {} {}>".format(self.id, ("Active" if self.active else ""))

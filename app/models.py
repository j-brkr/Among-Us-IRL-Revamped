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
    pin: so.Mapped[str] = so.mapped_column(sa.String(4))

    def __repr__(self):
        return "<User {}>".format(self.name)

'''
Plan

User:
- id
- name
- color
- pin
- icon_src

Task:
- id
- name
- type
- weight?

GameLog (json)

'''
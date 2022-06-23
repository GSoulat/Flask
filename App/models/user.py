from dataclasses import is_dataclass
from flask import abort
from flask_authorize import RestrictionsMixin, AllowancesMixin
from flask_authorize import PermissionsMixin
from flask_login import UserMixin, current_user
from App import db
# from flask_admin.contrib.sqla import ModelView


# mapping tables
UserGroup = db.Table(
    'user_group', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)


UserRole = db.Table(
    'user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    photo = db.Column(db.String(200))
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000),nullable=False)
    
    # `roles` and `groups` are reserved words that *must* be defined
    # on the `User` model to use group- or role-based authorization.
    roles = db.relationship('Role', secondary=UserRole)
    groups = db.relationship('Group', secondary=UserGroup)
    
    
class Group(db.Model, RestrictionsMixin):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class Role(db.Model, AllowancesMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    
class Article(db.Model, PermissionsMixin):
    __tablename__ = 'articles'
    __permissions__ = dict(
        owner=['read', 'update', 'delete', 'revoke'],
        group=['read', 'update'],
        other=['read']
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    content = db.Column(db.Text)
    
# class Controller(ModelView):
#     def is_accessible(self):
#         if current_user.is_admin == True:
#             return current_user.is_authenticated
#         else:
#             return abort(404)
#         return current_user.is_authenticated
#     def not_auth(self):
#         return "<h1>You are not authoreized to user the admin dachboard</h1>"
    
    
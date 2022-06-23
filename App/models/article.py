# from flask_authorize import PermissionsMixin
# from App import db

# class Article(db.Model, PermissionsMixin):
#     __tablename__ = 'articles'
#     __permissions__ = dict(
#         owner=['read', 'update', 'delete', 'revoke'],
#         group=['read', 'update'],
#         other=['read']
#     )

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), index=True, nullable=False)
#     content = db.Column(db.Text)
    
# class Controller(ModelView):
#     def is_accessible(self):
#         if current_user.is_admin == True:
#             return current_user.is_authenticated
#         else:
#             return abort(404)
#         return current_user.is_authenticated
#     def not_auth(self):
#         return "<h1>You are not authoreized to user the admin dachboard</h1>"
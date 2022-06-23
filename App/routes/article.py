# from flask import Blueprint, redirect, render_template, session, url_for, request, flash, abort
# from flask import jsonify
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
# from flask_authorize import Authorize
# from werkzeug import NotFound, Unauthorized
# from App.models.user import Article
# import App

# article = Blueprint('article', __name__, static_folder='/App/static', template_folder='App/templates')

# @article.route('/articles', methods=['POST'])
# @login.logged_in
# @authorize.create(Article)
# def article():
#     article = Article(
#       name=request.json.get('name'),
#       content=request.json.get('content'),
#     )
#     db.session.add(article)
#     db.session.commit()
#     return jsonify(msg='Created Article'), 200

# @article.route('/articles/<int:ident>', methods=['GET', 'PUT', 'DELETE'])
# @login.logged_in
# def single_article(ident):
#     article = db.session.query(Article).filter_by(id=ident).first()
#     if not article:
#         raise NotFound

#     if request.method == 'GET':

#         # check if the current user is authorized to read the article
#         if not authorize.read(article):
#             raise Unauthorized

#         return jsonify(id=article.id, name=article.name), 200

#     elif request.method == 'PUT':

#         # check if the current user is authorized to update to the article
#         if not authorize.update(article):
#             raise Unauthorized

#         # update values
#         if 'name' in request.json:
#             article.name = request.json['name']
#         if 'content' in request.json:
#             article.content = request.json['content']
#         db.session.commit()

#         return jsonify(id=article.id, name=article.name), 200

#     elif request.method == 'DELETE':

#         # check if the current user is associated with the 'admin' role
#         if not authorize.delete(article) or \
#            not authorize.has_role('admin'):
#             raise Unauthorized

#         db.session.delete(article)
#         db.session.commit()

#     return

# @article.route('/articles/<int:ident>/revoke', methods=['POST'])
# @login.logged_in
# def revoke_article(ident):
#     article = db.session.query(Article).filter_by(id=ident).first()
#     if not article:
#         raise NotFound

#     # check if the current user can revoke the article
#     if not authorize.revoke(article):
#         raise Unauthorized

#     article.revoked = True
#     db.session.commit()

#     return

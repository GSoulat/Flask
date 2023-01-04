from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from App import db
import logging as lg

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20),nullable=False)
    lastname = db.Column(db.String(20),nullable=False)
    work = db.Column(db.String(40),nullable=False)
    github = db.Column(db.String(100),nullable=False)
    created = db.Column(db.DateTime(timezone=True), default=db.func.now())
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(255), default="https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=80")
    active = db.Column(db.Boolean)
    isAdmin = db.Column(db.Boolean)

    def __repr__(self):
        return f'{self.id} {self.firstname}, {self.isAdmin}'

    def json(self):
        return {
            'id': self.id, 
            'firstname': self.firstname,
            'lastname': self.lastname,
            'work': self.work,
            'github': self.github,
            'created': self.created,
            'email': self.email,
            'password_hash': self.password_hash,
            'photo': self.photo,
            'active': self.active,
            'isAdmin': self.isAdmin
            }
        
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    
    # @property
    # def password(self):
    #     raise AttributeError("password is not readable attribute")
    
    # @password.setter
    # def password(self,password):
    #     self.password_hash = generate_password_hash(password)
    
    # def verify_password(self,password):
    #     return check_password_hash(self.password_hash,password)
    
 
def init_db():
    db.drop_all()
    db.create_all()
    
    first_user = User(
    id = 1,
    email = "gsoulat31@gmail.com",
    password_hash = generate_password_hash("123", method='sha256'),
    firstname = "Guillaume",
    isAdmin = 0 # 0 mean admin
    )
    first_user.save_to_db()

    second_user = User(
    id = 2,
    email = "gsoulat32@gmail.com",
    password_hash = generate_password_hash("123", method='sha256'),
    firstname = "coco",
    group = 1 # 1 mean user
    )
    second_user.save_to_db()

lg.warning('Database initialized!')
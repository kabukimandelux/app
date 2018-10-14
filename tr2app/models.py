#Added to git
from tr2app import db, login_manager
from flask_login import UserMixin
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(40), nullable=False)
    postcode = db.Column(db.String(8), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    membertype = db.Column(db.String(20),nullable=False)
    bills = db.relationship('Billing',backref='account',lazy=True)
    attendance = db.relationship('Attendance',backref='attended',lazy=True)

    def __repr__(self):
        return f"Member('{self.id}',{self.name}', '{self.email}', '{self.image_file}')"

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String(100),nullable=False)

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(40), nullable=False)
    amount = db.Column(db.Float(10), nullable=False, default=0)
    image_file = db.Column(db.String(20), default='default.jpg')
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    member_list = db.relationship('Member',foreign_keys=[member_id])

    def __repr__(self):
        return f"Bill('{self.member_id}', '{self.date}', '{self.amount}')"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(40), nullable=False)
    type = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    billed_status = db.Column(db.Boolean, nullable=False)
    attendance = db.relationship('Attendance',backref='presence',lazy=True)

    def __repr__(self):
        return f"Event('{self.id}', '{self.date}', '{self.name}')"

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event_list = db.relationship('Event',foreign_keys=[event_id])
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    member_list = db.relationship('Member',foreign_keys=[member_id])
    status = db.Column(db.String(10), nullable=False, default=0)
    __table_args__ = (db.UniqueConstraint('event_id','member_id'),)
    

    def __repr__(self):
        return f"Attendance('{self.member_id}', '{self.event_id}', '{self.status}')"

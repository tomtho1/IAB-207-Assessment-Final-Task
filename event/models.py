import enum

from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    # password is never stored in the DB, an encrypted password is stored
    # the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    image = db.Column(db.LargeBinary)

    street_number = db.Column(db.String(20), index=True, nullable=False)
    street = db.Column(db.String(100), index=True, nullable=False)
    city = db.Column(db.String(100), index=True, nullable=False)
    state = db.Column(db.String(100), index=True, nullable=False)
    post_code = db.Column(db.String(20), index=True, nullable=False)

    # relation to call user.comments and comment.created_by
    # comments = db.relationship('Comment', backref='user')

    def __repr__(self):  # string print method
        return "ID: {}\t Name: {}\tEmail: {}".format(self.id, self.name, self.email)


class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    desc = db.Column(db.String)
    user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    image = db.Column(db.LargeBinary)

    events = db.relationship('Event', backref='artist_event')

class Venue(db.Model):
    __tablename__ = "venues"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)  # venue name is unique
    user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    street_number = db.Column(db.String(20), index=True, nullable=False)
    street = db.Column(db.String(100), index=True, nullable=False)
    city = db.Column(db.String(100), index=True, nullable=False)
    state = db.Column(db.String(100), index=True, nullable=False)
    post_code = db.Column(db.String(20), index=True, nullable=False)
    image = db.Column(db.LargeBinary)    
class EventStatus(enum.Enum):
    open = 0
    unpublished = 1
    sold_out = 2
    cancelled = 3


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    artist = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.max)
    venue = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    price = db.Column(db.Integer, nullable=False)  # Store cents as integers to avoid floating point errors.
    tickets = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(EventStatus), nullable=False, default=EventStatus.open)

    desc = db.Column(db.String, default="No description available.")

    image = db.Column(db.LargeBinary)

    # ... Create the Events db.relationship
    # relation to call event.comments and comment.event
    comments = db.relationship('Comment', backref='event_comments')
    bookings = db.relationship('Booking', backref='event_bookings')


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String)
    datetime = db.Column(db.DateTime, default=datetime.now())

    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    event = db.Column(db.Integer, db.ForeignKey('events.id'))


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, default=datetime.now())
    tickets = db.Column(db.Integer, default=1)

    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    event = db.Column(db.Integer, db.ForeignKey('events.id'))

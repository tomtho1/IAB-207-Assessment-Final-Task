import unittest
from datetime import datetime
from multiprocessing import Event

from werkzeug.security import generate_password_hash, check_password_hash

from event import db, create_app
from event.models import User, Artist, Venue, Event, Comment, Booking

time_now = datetime.now()
test_db = "test.sqlite"
db_full_path = ("event\\"+test_db)

test_user = User(name='testuser', email="test@test.com", password_hash=generate_password_hash("test"), street_number="1", street="test street", city="test city", state="QLD", post_code="1111")
test_artist = Artist(name="test artist", genre="genre", desc="test", user=1)
test_venue = Venue(name="test venue", user=1, street_number="1", street="test street", city="test city", state="QLD", post_code="1111")
test_event = Event(name="test event", artist=1, datetime=time_now, venue=test_venue.name, price=2_00, tickets=1000, desc="test")
test_comment = Comment(text='this is a test.', datetime=time_now, user=1, event=1)
test_booking = Booking(datetime=time_now, user=1, event=1)

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
ctx = app.app_context()
ctx.push()

db.drop_all()
db.create_all()


class TestUser(unittest.TestCase):
    # Database tests
    db.session.add(test_user)
    db.session.add(test_artist)
    db.session.add(test_venue)
    db.session.add(test_event)
    db.session.add(test_comment)
    db.session.add(test_booking)
    db.session.commit()

    # Read User Data
    def test_user_data(self):
        read_data = User.query.filter_by(name='testuser').first()
        self.assertEqual(read_data.name, 'testuser')
        self.assertEqual(read_data.email, 'test@test.com')
        assert check_password_hash(read_data.password_hash, 'test')
        self.assertEqual(read_data.street_number, '1')
        self.assertEqual(read_data.street, 'test street')
        self.assertEqual(read_data.city, 'test city')
        self.assertEqual(read_data.state, 'QLD')        
        self.assertEqual(read_data.post_code, '1111')

    # Read Artist Data
    def test_artist_data(self) -> None:
        read_data = Artist.query.get(1)
        self.assertEqual(read_data.name, "test artist")
        self.assertEqual(read_data.genre, "genre")
        self.assertEqual(read_data.desc, "test")
        self.assertEqual(read_data.user, 1)

# test_venue = Venue(name="test venue", user=1, street_number="1", street="test street", city="test city", state="QLD", post_code="1111")
    # Read Venue Data
    def test_venue_data(self) -> None:
        read_data = Venue.query.filter_by(name="test venue").first()
        self.assertEqual(read_data.name, "test venue")
        self.assertEqual(read_data.user, 1)
        self.assertEqual(read_data.street_number, "1")
        self.assertEqual(read_data.street, "test street")
        self.assertEqual(read_data.city, "test city")
        self.assertEqual(read_data.state, "QLD")
        self.assertEqual(read_data.post_code, "1111")

    # Read Event Data
    def test_event_data(self) -> None:
        read_data = Event.query.filter_by(name="test event").first()
        self.assertEqual(read_data.name, "test event")
        self.assertEqual(read_data.artist, 1)
        self.assertEqual(read_data.datetime, time_now)
        self.assertEqual(read_data.venue, "test venue")
        self.assertEqual(read_data.price, 2_00)
        self.assertEqual(read_data.desc, "test")

    # Read Comment Data
    def test_comment_data(self):
        read_data = Comment.query.filter_by(text='this is a test.').first()
        self.assertEqual(read_data.text, 'this is a test.')
        self.assertEqual(read_data.datetime, time_now)
        self.assertEqual(read_data.user, 1)
        self.assertEqual(read_data.event, 1)
    
    # Read Booking Data
    def test_booking_data(self):
        read_data = Booking.query.filter_by(datetime=time_now).first()
        self.assertEqual(read_data.datetime, time_now)
        self.assertEqual(read_data.user, 1)
        self.assertEqual(read_data.event, 1)


if __name__ == '__main__':
    unittest.main()

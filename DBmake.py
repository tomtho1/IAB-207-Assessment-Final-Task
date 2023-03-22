from datetime import datetime

from werkzeug.security import generate_password_hash

from event import db, create_app
from event.models import User, Venue, Artist, Event, Comment, Booking, EventStatus

app = create_app()
ctx = app.app_context()
ctx.push()


def convert_blob(filename: str):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def create_users():
    users = [User(id=1, name="Evil_Cat", email="test@test.com", password_hash=generate_password_hash("test"),
                  image=convert_blob(
                      "temp_img/comments/DALL·E 2022-09-16 11.26.58 - an evil cat with superpowers, lightning is lighting up the sky, digital art.webp"),
                  street_number=1, street="Test Street", city="Test City", state="TEST", post_code=4000),

             User(id=2, name="CroissantMachine", email="test1@test.com", password_hash=generate_password_hash("test"),
                  image=convert_blob(
                      "temp_img/comments/DALL·E 2022-11-02 12.20.05 - profile picture of a user, digital art.webp"),
                  street_number=1, street="Test Street", city="Test City", state="TEST", post_code=4000),

             User(id=3, name="MusicGirl", email="test1@test.com", password_hash=generate_password_hash("test"),
                  image=convert_blob(
                      "temp_img/comments/DALL·E 2022-11-02 12.22.06 - profile picture of a user, digital art.webp"),
                  street_number=1, street="Test Street", city="Test City", state="TEST", post_code=4000)]

    for user in users:
        db.session.add(user)
    db.session.flush()


def create_artists():
    artists = [Artist(id=1, name="The Programmers", genre="Rock", user=2,
                      desc="We are a band of programmers who love to rock out!",
                      image=convert_blob("temp_img/DALL·E 2022-11-01 19.43.43 - the profile picture of a rock band, digital art.webp")),
               Artist(id=2, name="Keystroke", genre="Rock", user=3,
                      desc="Keystroke is the classic rock band that truly redefined the genre, and for good reason.",
                      image=convert_blob("temp_img/DALL·E 2022-11-01 19.46.49 - the profile picture of a techno band, digital art, synthwave.webp")),
               Artist(id=3, name="Python", genre="Death Metal", user=1,
                      desc="Bringing you the most brutal music since 2000 BC, Python is a six man crew that is "
                           "constantly pushing boundaries and creating some of the most extreme music in the world.",
                      image=convert_blob("temp_img/DALL·E 2022-11-01 19.43.48 - the profile picture of a rock band, digital art.webp")),
               Artist(id=4, name="CSExtra", genre="Techno", user=2,
                      desc="Inspired by the sounds of chiptunes, CSExtra is a techno-pop band that fuses elements of "
                           "reggae, dub and dancehall.",
                      image=convert_blob("temp_img/DALL·E 2022-11-01 19.46.54 - the profile picture of a techno band, digital art, synthwave.webp")),
               Artist(id=5, name="Hot Coffee", genre="Jazz", user=1,
                      desc="Hot Coffee is a completely improvised and unscripted jazz band. The songs are song "
                           "collections where the musicians take turns leading with rhythm and melody, sounding like "
                           "a group of friends sitting in a kitchen together.",
                      image=convert_blob("temp_img/DALL·E 2022-11-01 19.47.33 - the profile picture of a jazz band, digital art.webp")),
               Artist(id=6, name="Keyboard Warriors", genre="Soft Rock", user=3,
                      desc="Keyboard Warriors is a soft rock band that is inspired by the sounds of the 80s and 90s.",
                      image=convert_blob("temp_img/DALL·E 2022-11-01 19.46.56 - the profile picture of a techno band, digital art, synthwave.webp")),
               ]

    for artist in artists:
        db.session.add(artist)
    db.session.flush()


def create_venues():
    venues = [Venue(id=1, name="City Park Main Stage", user=2, street_number=22, street="Big Street", city="Brisbane",
                    state="Queensland", post_code=4000, image=convert_blob("temp_img/venue-outdoor-stage.jpg")),
              Venue(id=2, name="City Park Jazz Stage", user=1, street_number=22, street="Big Street", city="Brisbane",
                    state="Queensland", post_code=4000, image=convert_blob("temp_img/DALL·E 2022-09-16 11.04.33 - an indoor jazz festival at night time, lots of lights, digital art.webp"))]

    for venue in venues:
        db.session.add(venue)
    db.session.flush()


def create_events():
    events = [
        Event(id=1, name="Problematic Program", artist=1, venue=1, datetime=datetime(2022, 12, 10, 19, 30), price=42995,
              tickets=1024, image=convert_blob(
                "temp_img/DALL·E 2022-09-16 10.54.14 - an outdoor music festival in the day, digital art.webp"),
              desc="The Programmers are back to perform their new hit single \"I've Gotta Code (500 Lines)\" which "
                   "recently topped charts in Antarctica! The Programmers are a Brittish rock duo formed by Roy "
                   "Trenneman and Maurice Moss who first came to attention with their single \"Email from a "
                   "Spammer\"."),

        Event(id=2, name="DEFCON2", artist=2, venue=1, datetime=datetime(2022, 12, 2, 21, 30), price=56099, tickets=1200,
              desc="The latest songs and those classics from the past are all here. "
                   "Come and see the incredible band keystroke live at Riverstage.",
              image=convert_blob(
                  "temp_img/DALL·E 2022-09-16 10.49.06 - an outdoor music festival at night time, lots of lights, pixel art.webp")),

        Event(id=3, name="SLitherin", artist=3, venue=1, datetime=datetime(2023, 2, 8, 2, 30), price=56099, tickets=1200,
              desc="Bringing you the most brutal music since 2000 BC, Python is a death metal band. Their music is "
                   "avant-garde and violent,with a group of individuals who come together to play in an effort to "
                   "help each other feel less lonely.", status=EventStatus.cancelled,
              image=convert_blob(
                  "temp_img/DALL·E 2022-09-16 10.58.41 - an outdoor music festival in the day, digital art.webp")),

        Event(id=4, name="Java", artist=5, venue=2, datetime=datetime(2023, 2, 8, 12, 30), price=56099, tickets=200,
              desc="Hot Coffee is a completely improvised and unscripted jazz band. The songs are song collections "
                   "where the musicians take turns leading with rhythm and melody, sounding like a group of friends "
                   "sitting in a kitchen together.", status=EventStatus.sold_out,
              image=convert_blob(
                  "temp_img/DALL·E 2022-09-16 11.04.21 - an indoor jazz festival at night time, lots of lights, digital art.webp")),
    ]

    for event in events:
        db.session.add(event)
    db.session.flush()


def create_comments():
    comments = [Comment(text="I can't wait to see this year's show! Last year's was amazing, especially the part "
                             "where the guy with the glasses got on stage and did his thing and people started "
                             "chanting \"Moss! Moss! Moss!\". It was so awesome, and I was so happy I got to see them "
                             "perform.",
                        datetime=datetime(2022, 10, 30, 5, 12), user=1, event=1)]

    for comment in comments:
        db.session.add(comment)
    db.session.flush()


def create_bookings():
    db.session.add(Booking(user=1, event=1))
    for i in range(100):
        db.session.add(Booking(user=1, event=4))
        db.session.add(Booking(user=3, event=4))
    db.session.flush()


def create():
    db.create_all()
    create_users()
    create_artists()
    create_venues()
    create_events()
    create_comments()
    create_bookings()
    db.session.commit()


def create_if_empty():
    db.create_all()
    # If user doesn't exist assume database is empty
    if not db.session.query(User.query.filter_by(id=1).exists()).scalar():
        create()


if __name__ == "__main__":
    db.drop_all()
    create()

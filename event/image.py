import filetype
from flask import Blueprint, Response, abort

from . import db
from .models import Artist, Event, User, Venue

bp = Blueprint('img', __name__, url_prefix='/img')


@bp.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event(event_id: int):
    if image := db.session.query(Event.image).filter_by(id=event_id).scalar():
        return Response(image, mimetype=filetype.image_match(image).mime)
    return abort(404)
    # return send_file("static/img/blank.svg")


# TODO: Remove duplicated code
@bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user(user_id: int):
    if image := db.session.query(User.image).filter_by(id=user_id).scalar():
        return Response(image, mimetype=filetype.image_match(image).mime)
    return abort(404)


@bp.route('/artist/<int:artist_id>', methods=['GET', 'POST'])
def artist(artist_id: int):
    if image := db.session.query(Artist.image).filter_by(id=artist_id).scalar():
        return Response(image, mimetype=filetype.image_match(image).mime)
    return abort(404)


@bp.route('/venue/<int:venue_id>', methods=['GET', 'POST'])
def venue(venue_id: int):
    if image := db.session.query(Venue.image).filter_by(id=venue_id).scalar():
        return Response(image, mimetype=filetype.image_match(image).mime)
    return abort(404)
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from werkzeug import Response

from . import db
from .forms import CreateArtistForm
from .models import Artist, Event

bp = Blueprint('artist', __name__, url_prefix='/artists')


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create() -> Response | str:
    form = CreateArtistForm()
    if form.validate_on_submit():
        artist = Artist(name=form.name.data, genre=form.genre.data, user=current_user.id,
                        desc=form.desc.data, image=request.files[form.image.name].read())
        db.session.add(artist)
        db.session.commit()
        return redirect(url_for('artist.get_artist', artist_id=artist.id, genres=genres))
    return render_template("create_form.html", title="Create Artist | Elevental", heading="Create an Artist", form=form)


@bp.route('/<artist_id>')
def get_artist(artist_id) -> str:
    # get artist name genre image from db
    artist = Artist.query.get(artist_id)   

    # show all events status is open, cancelled or sold_out
    events = Event.query.filter_by(artist=artist_id).filter(
        Event.status.in_(['open', 'sold_out', 'cancelled'])).all()
    return render_template("event.html", title=f"{artist.name} | Elevental", artist=artist, events=events)

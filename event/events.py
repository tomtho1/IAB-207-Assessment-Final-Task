from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import current_user, login_required
from sqlalchemy.sql import functions as func
from werkzeug import Response

from . import db
from .forms import CreateEventForm, EditEventForm
from .models import Event, Artist, User, Venue, Comment, Booking, EventStatus

bp = Blueprint('event', __name__, url_prefix='/events')


def get_username(user_id: int) -> str:
    return db.session.query(User.name).filter_by(id=user_id).scalar()


def get_tickets_sold(event_id: int) -> int:
    return db.session.query(func.sum(Booking.tickets)).filter_by(event=event_id).scalar() or 0


@bp.route('/')
def all() -> Response | str:
    # TODO: Add unpublished events for event owners
    events = Event.query.join(Artist, Artist.id == Event.artist) \
        .filter(Event.status != EventStatus.unpublished).all()

    return render_template('events_list.html', page_title=f"All Events", events=events)

@bp.route('/my_events', methods=['GET', 'POST'])
@login_required
def my_events() -> Response | str:
    events = Event.query.join(Artist, Artist.id == Event.artist).filter_by(user=current_user.id).all()
    return render_template('events_list.html', page_title=f"My Events", events=events)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create() -> Response | str:
    form = CreateEventForm()
    form.venue.choices = [(k, v) for k, v in db.session.query(Venue.id, Venue.name).filter_by(user=current_user.id).all()]     
    form.artist.choices = [(k, v) for k, v in db.session.query(Artist.id, Artist.name).filter_by(user=current_user.id).all()] 
    if form.validate_on_submit():
        if db.session.query(Artist.query.filter_by(id=form.artist.data, user=current_user.id).exists()).scalar():
            event = Event(name=form.name.data, artist=int(form.artist.data),
                          datetime=datetime.combine(form.date.data, form.time.data),
                          venue=int(form.venue.data), price=int(form.price.data * 100), user=current_user.id,
                          tickets=form.tickets.data, desc=form.desc.data, status=EventStatus(int(form.status.data)),
                          image=request.files[form.image.name].read())
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('event.get_event', event_id=event.id))
        else:
            form.artist.errors.append("Invalid Artist")
    return render_template("create_form.html", title="Create Event | Elevental", heading="Create an Event", form=form)


@bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(event_id) -> Response | str:
    if (event := Event.query.get(event_id)) is None:  # Event not found
        return abort(404)
    if db.session.query(Artist.user).filter_by(id=event.artist).scalar() != current_user.id:  # Artist not owned by user
        return abort(403)

    form = EditEventForm()
    form.venue.choices = [v[0] for v in db.session.query(Venue.name).all()]
    form.artist.choices = [(k, v) for k, v in db.session.query(Artist.id, Artist.name).filter_by(user=current_user.id).all()] 

    if form.validate_on_submit():
        if db.session.query(Artist.query.filter_by(id=form.artist.data, user=current_user.id).exists()).scalar():
            event.name = form.name.data
            event.artist = form.artist.data
            event.datetime = datetime.combine(form.date.data, form.time.data)
            event.venue = form.venue.data
            event.price = int(form.price.data * 100)
            event.tickets = form.tickets.data
            event.status = EventStatus(int(form.status.data))
            event.desc = form.desc.data

            if form.image.data:
                event.image = request.files[form.image.name].read()

            db.session.commit()
            return redirect(url_for('event.get_event', event_id=event.id))
        else:
            form.artist.errors.append("Invalid Artist")

    form.name.data = event.name
    form.artist.data = event.artist
    form.date.data = event.datetime.date()
    form.time.data = event.datetime.time()
    form.venue.data = event.venue
    form.price.data = event.price / 100
    form.tickets.data = event.tickets
    form.desc.data = event.desc

    return render_template("create_form.html", title="Edit Event | Elevental", heading="Edit an Event", form=form)


@bp.route('/<int:event_id>')
def get_event(event_id: int) -> str | Response | None:
    if (event := Event.query.get(event_id)) is None:  # Event not found
        return abort(404)

    artist = Artist.query.get(event.artist)
    price = divmod(event.price, 100)  # Convert cents to dollars and cents
    tickets_avail = event.tickets - get_tickets_sold(event_id)
    venue = db.session.query(Venue.name).filter_by(id=event.venue).scalar()

    return render_template("event.html", title=f"{event.name} | Elevental", get_username=get_username, event=event,
                           artist=artist, price=price, venue=venue, tickets_avail=tickets_avail)


@bp.route('/<int:event_id>/comment', methods=['GET', 'POST'])
@login_required
def create_comment(event_id: int) -> Response:
    if request.method == "GET":
        flash("Please try commenting again")
        return redirect(url_for('event.get_event', event_id=event_id))

    if not db.session.query(Event.query.filter_by(id=event_id).exists()).scalar():
        return abort(404)

    if len((comment := request.form.get('comment'))) > 0:
        db.session.add(Comment(text=comment, datetime=datetime.now(),
                               user=current_user.id, event=event_id))
        db.session.commit()
    else:
        flash("Comment cannot be empty.")

    return redirect(url_for('event.get_event', event_id=event_id))


@bp.route('/<int:event_id>/book', methods=['GET', 'POST'])
@login_required
def create_booking(event_id: int) -> Response:
    if request.method == "GET":
        flash("Please try booking again")
        return redirect(url_for('event.get_event', event_id=event_id))

    if (event := Event.query.get(event_id)) is None:
        return abort(404)

    if event.status != EventStatus.open:
        flash("Event is not open for bookings.")
        return redirect(url_for('event.get_event', event_id=event_id))

    total_tickets_sold = get_tickets_sold(event_id)

    if (tickets := request.form.get('tickets')) is not None \
            and tickets.isdigit() \
            and 0 < (tickets := int(tickets)) <= (event.tickets - total_tickets_sold)\
            and tickets <= 10:
        db.session.add(Booking(tickets=int(tickets), datetime=datetime.now(),
                               user=current_user.id, event=event_id))

        if (total_tickets_sold + tickets) >= event.tickets:
            event.status = EventStatus.sold_out

        db.session.commit()

        flash("Booking successful.")
        
    else:
        flash("Invalid number of tickets.")

    return redirect(url_for('event.get_event', event_id=event_id))

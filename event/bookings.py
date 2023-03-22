from flask import Blueprint, render_template

from .models import Artist, Booking, Event
from flask_login import login_required, current_user
from . import db

bp = Blueprint('booking', __name__, url_prefix='/bookings')

@bp.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    tickets = db.session.query(Booking, Event, Artist).filter_by(user=current_user.id)\
        .join(Event, Event.id == Booking.event)\
        .join(Artist, Artist.id == Event.artist).all()
         
    return render_template("bookings.html", title="Your History | Elevental", tickets=tickets)

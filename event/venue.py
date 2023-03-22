from flask import Blueprint, flash, render_template, request, url_for, redirect
# from .models import User
from flask_login import current_user, login_required

from event.models import Venue, Event
from . import db
from .forms import CreateVenueForm

# create a blueprint
bp = Blueprint('venue', __name__, url_prefix='/venue')


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    create_venue_form = CreateVenueForm()

    if (create_venue_form.validate_on_submit() == True):        
        image = request.files[create_venue_form.image.name].read()
        name = create_venue_form.name.data
        user = current_user.id
                
        street_number = create_venue_form.street_number.data
        street = create_venue_form.street.data
        city = create_venue_form.city.data
        state = create_venue_form.state.data
        post_code = create_venue_form.post_code.data

        # check if venue exists
        v1 = Venue.query.filter_by(name=name).first()
        if v1:
            flash('Venue already exists')
            return redirect(url_for('venue.create_venue'))        
        
        # create a new venue model object
        new_venue = Venue(image=image, name=name, user=user,
                        street_number=street_number, street=street, city=city, state=state, post_code=post_code)
        db.session.add(new_venue)
        db.session.commit()
        # commit to the database and redirect to HTML page
        return redirect(url_for('main.index'))
    # the else is called when there is a get message
    else:
        # return redirect(url_for('main.index'))
        return render_template('create_venue.html', form=create_venue_form, heading='Create Venue', genres=genres, artists=artists)


@bp.route('/<int:venue_id>')
def get_venue(venue_id: int) -> str:
    # get artist name genre image from db
    venue = Venue.query.get(venue_id)    
    # get evenets that are from this venue
    events = Event.query.filter_by(venue=venue_id).all()
    return render_template("venue.html", title=f"{venue.name} | Elevental", venue=venue, events=events)
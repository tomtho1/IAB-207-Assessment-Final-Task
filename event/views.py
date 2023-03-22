from flask import Blueprint, render_template, request, redirect, url_for, flash

from . import app
from .models import Event, Artist, EventStatus, Venue

bp = Blueprint('main', __name__)


@app.context_processor
def inject_vars():
    return {"StatusColours": ["bg-primary", "bg-info", "bg-warning", "bg-danger"],
            "StatusText": ["Open", "Unpublished", "Sold-out", "Cancelled"],
            "genres": Event.query.join(Artist).filter(Event.status != EventStatus.unpublished).with_entities(Artist.genre).distinct().all(),
            "artists": Artist.query.all()}


@bp.route('/')
def index():
    events = Event.query.filter(Event.status != EventStatus.unpublished).all()
    venues = Venue.query.all()
    return render_template('index.html', events=events, venues=venues)


@bp.route('/genre/<genre>')
def genre(genre):

    filtered_events = Event.query.join(Artist, Artist.id == Event.artist)\
        .filter(Artist.genre.contains(genre))\
        .filter(Event.status != EventStatus.unpublished).all()

    return render_template('events_list.html', page_title=f"{genre} Performances",
                           events=filtered_events)


@bp.route('/search')
def search():
    if query := request.args.get('search'):
        if len(query) >= 3:
            
            search_term = f"%{query}%"

            results = Event.query.join(Artist, Artist.id == Event.artist)\
                .join(Venue, Venue.id == Event.venue)\
                .filter((Artist.name.ilike(search_term)
                        | Artist.genre.ilike(search_term)
                        | Event.name.ilike(search_term)
                        | Venue.name.ilike(search_term))
                        & (Event.status != EventStatus.unpublished)).all()

            return render_template('events_list.html', page_title=f"Search results for '{query}'",
                                   events=results)

        else:                        
            flash("Search must 3 characters or more.")
            return redirect(url_for('main.index'))

    else:
        flash("Please enter a search term.")
        return redirect(url_for('main.index'))

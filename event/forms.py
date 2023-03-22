import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import IntegerField
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, \
    DateField, TimeField, FileField, SelectField, DecimalField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange, Length, Regexp, ValidationError

USER_FORM_STRINGFIELD_DEFAULTS = ["mt-1", "mb-3"]
USER_FORM_STRINGFIELD_DEFAULTS_ADDRESS = ["mt-1", "mb-2"]


# Factory Pattern for creating stringfields for forms
def create_stringfield(label=None, validators=[], styles_class=[]):

    # for each style in the list, add it to the string
    styles = " ".join(styles_class)

    styles_dict = {"class": styles}
    return StringField(label, validators=validators, render_kw=styles_dict)


# creates the login information
class LoginForm(FlaskForm):
    user_name = create_stringfield("User Name", validators=[InputRequired(
        'Enter user name')], styles_class=USER_FORM_STRINGFIELD_DEFAULTS)
    password = PasswordField("Password", validators=[InputRequired('Enter user password')],
                             render_kw={"class": " ".join(USER_FORM_STRINGFIELD_DEFAULTS)})
    submit = SubmitField("Login", render_kw={"class": "mt-3"})


# this is the registration form
class RegisterForm(FlaskForm):
    STATES_SELECT = ('Australian Capital Teritory', 'New South Wales', 'Northern Territory',
              'Queensland', 'South Australia', 'Tasmania', 'Victoria', 'Western Australia')

    user_name = create_stringfield("User Name", validators=[
                                   InputRequired(), Length(min=3, max=100)], styles_class=['mt-1','mb-3', 'd-flex'])
    image = FileField('Avatar Image', validators=[InputRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')],render_kw= {"class": "d-flex justify-content-center mb-3"})

    
    street_number = create_stringfield("Steet Number", validators=[InputRequired(), Regexp(
        '^[0-9a-zA-Z/]+$', message='Not a valid street number')], styles_class= ['mt-1', 'mb-2', 'w-25', 'd-flex'])

    street = create_stringfield("Steet", validators=[InputRequired(), Regexp(
        '^[a-zA-Z]+[ ]+[a-zA-Z]*', message="Invalid street.")], styles_class=USER_FORM_STRINGFIELD_DEFAULTS_ADDRESS)
    city = create_stringfield("City", validators=[InputRequired(), Regexp(
        '^[a-zA-Z ]+$', message="Invalid city.")], styles_class=USER_FORM_STRINGFIELD_DEFAULTS_ADDRESS)    
    state = SelectField("State", choices=STATES_SELECT, validators=[InputRequired()], render_kw={
                        "class": " ".join(USER_FORM_STRINGFIELD_DEFAULTS_ADDRESS)})

    post_code = create_stringfield("Post Code", validators=[InputRequired(), Regexp(
        '(\d{4})', message='Not a valid post code'), Length(max=4)], styles_class=['mt-1', 'mb-5', 'w-25', 'd-flex'])

    
    email_id = create_stringfield("Email Address", validators=[Email(
        "Please enter a valid email")], styles_class=USER_FORM_STRINGFIELD_DEFAULTS)
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords must match")],
                             render_kw={"class": "mb-2 mt-2"})
    confirm = PasswordField("Confirm Password", validators=[InputRequired()],
                            render_kw={"class": " ".join(USER_FORM_STRINGFIELD_DEFAULTS)})
    submit = SubmitField("Register", render_kw={"class": "mt-3"})


class CreateEventForm(FlaskForm):
    name = StringField("Event Name", validators=[InputRequired()])
    artist = SelectField("Artist", validators=[InputRequired()])
    date = DateField("Date", validators=[InputRequired()])
    time = TimeField("Time", validators=[InputRequired()])
    status = SelectField("Status", validators=[InputRequired()],
                         choices=[(i, text) for i, text in enumerate(["Open", "Unpublished", "Sold-Out", "Cancelled"])])
    venue = SelectField("Venue", validators=[InputRequired()])
    price = DecimalField("Price", validators=[
                         InputRequired(), NumberRange(min=0)], places=2)
    tickets = IntegerField("Tickets", validators=[
                           InputRequired(), NumberRange(min=0)])
    desc = TextAreaField("Description")

    image = FileField(validators=[InputRequired()])

    submit = SubmitField("Create")

    def validate_date(self, field):
        if field.data < datetime.date.today():
            raise ValidationError("Date must not be in the past.")


class EditEventForm(CreateEventForm):
    image = FileField()
    submit = SubmitField("Edit")


class CreateArtistForm(FlaskForm):
    name = StringField("Artist Name", validators=[InputRequired()])
    genre = StringField("Genre", validators=[InputRequired()])
    desc = TextAreaField("Description")

    image = FileField(validators=[InputRequired(message="Please upload an image.")])

    submit = SubmitField("Create")

class CreateVenueForm(FlaskForm):
    STATES_SELECT = ('Australian Capital Teritory', 'New South Wales', 'Northern Territory',
              'Queensland', 'South Australia', 'Tasmania', 'Victoria', 'Western Australia')

    name = create_stringfield("Venue Name", validators=[
                                   InputRequired(), Length(min=3, max=100)], styles_class=['mt-1','mb-3', 'd-flex'])
    image = FileField('Venue Image', validators=[InputRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')],render_kw= {"class": "d-flex justify-content-center mb-3"})

    
    street_number = create_stringfield("Steet Number", validators=[InputRequired(), Regexp(
        '^[0-9a-zA-Z/]+$', message='Not a valid street number')], styles_class= ['mt-1', 'mb-2', 'w-25', 'd-flex'])

    street = create_stringfield("Steet", validators=[InputRequired(), Regexp(
        '^[a-zA-Z]+[ ]+[a-zA-Z]*', message="Invalid street.")], styles_class=USER_FORM_STRINGFIELD_DEFAULTS_ADDRESS)
    city = create_stringfield("City", validators=[InputRequired(), Regexp(
        '^[a-zA-Z ]+$', message="Invalid city.")], styles_class=USER_FORM_STRINGFIELD_DEFAULTS_ADDRESS)    
    state = SelectField("State", choices=STATES_SELECT, validators=[InputRequired()], render_kw={
                        "class": " ".join(USER_FORM_STRINGFIELD_DEFAULTS_ADDRESS)})

    post_code = create_stringfield("Post Code", validators=[InputRequired(), Regexp(
        '(\d{4})', message='Not a valid post code'), Length(max=4)], styles_class=['mt-1', 'mb-5', 'w-25', 'd-flex'])

    submit = SubmitField("Create", render_kw={"class": "mt-3"})
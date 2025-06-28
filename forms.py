from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SelectMultipleField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('User Type', choices=[
        ('founder', 'Startup Founder'),
        ('investor', 'Investor'),
        ('partner', 'Business Partner'),
        ('service_provider', 'Service Provider')
    ], validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    location = StringField('Location')
    industry = SelectField('Industry', choices=[
        ('', 'Select Industry'),
        ('technology', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('retail', 'Retail'),
        ('manufacturing', 'Manufacturing'),
        ('energy', 'Energy'),
        ('real_estate', 'Real Estate'),
        ('agriculture', 'Agriculture'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other')
    ])
    experience = TextAreaField('Experience/Expertise', validators=[Length(max=1000)])
    submit = SubmitField('Register')

class StartupForm(FlaskForm):
    """Startup creation/edit form"""
    name = StringField('Startup Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=2000)])
    industry = SelectField('Industry', choices=[
        ('technology', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('retail', 'Retail'),
        ('manufacturing', 'Manufacturing'),
        ('energy', 'Energy'),
        ('real_estate', 'Real Estate'),
        ('agriculture', 'Agriculture'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    stage = SelectField('Stage', choices=[
        ('idea', 'Idea Stage'),
        ('prototype', 'Prototype'),
        ('mvp', 'MVP (Minimum Viable Product)'),
        ('scaling', 'Scaling'),
        ('established', 'Established')
    ], validators=[DataRequired()])
    funding_needed = StringField('Funding Needed', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    website = StringField('Website (Optional)')
    pitch_deck = StringField('Pitch Deck URL (Optional)')
    team_size = IntegerField('Team Size', validators=[DataRequired(), NumberRange(min=1)])
    revenue = StringField('Current Revenue (Optional)')
    looking_for = SelectMultipleField('Looking For', choices=[
        ('investors', 'Investors'),
        ('partners', 'Business Partners'),
        ('service_providers', 'Service Providers')
    ], validators=[DataRequired()])
    submit = SubmitField('Save Startup')

class ConnectionForm(FlaskForm):
    """Connection request form"""
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Send Connection Request')

class MessageForm(FlaskForm):
    """Direct message form"""
    content = TextAreaField('Message', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Send Message')

class SearchForm(FlaskForm):
    """Search form"""
    query = StringField('Search Keywords')
    industry = SelectField('Industry', choices=[
        ('', 'All Industries'),
        ('technology', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('retail', 'Retail'),
        ('manufacturing', 'Manufacturing'),
        ('energy', 'Energy'),
        ('real_estate', 'Real Estate'),
        ('agriculture', 'Agriculture'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other')
    ])
    stage = SelectField('Stage', choices=[
        ('', 'All Stages'),
        ('idea', 'Idea Stage'),
        ('prototype', 'Prototype'),
        ('mvp', 'MVP'),
        ('scaling', 'Scaling'),
        ('established', 'Established')
    ])
    looking_for = SelectField('Looking For', choices=[
        ('', 'All Types'),
        ('investors', 'Investors'),
        ('partners', 'Business Partners'),
        ('service_providers', 'Service Providers')
    ])
    submit = SubmitField('Search')

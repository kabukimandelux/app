#Added to git 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from tr2app.models import Member
import datetime

class AddMemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    firstname = StringField('Name', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    postcode = StringField('postcode', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image_file = StringField('image_file')
    membertype = SelectField('Member Tyoe',choices=[('1','Actif'),('2','Ancien'),('3','Candidat'),('4','Honoraire'),('5','Non Membre')])
    register = SubmitField('Add Member')
    def validate_email(self, email):
        email = Member.query.filter_by(email=email.data).first()
        if email:
                raise ValidationError('Email already exists')

class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EditMemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    firstname = StringField('Name', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    postcode = StringField('postcode', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image_file = StringField('image_file')
    membertype = SelectField('Member Tyoe',choices=[('1','Actif'),('2','Ancien'),('3','Candidat'),('4','Honoraire')])
    register = SubmitField('Update')

class UserForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        register = SubmitField('Add Member')
        def validate_username(self, username):
                username = Member.query.filter_by(username=username.data).first()
                if username:
                        raise ValidationError('Username already exists')

class BillingForm(FlaskForm):
    date = DateField('Date')
    description = StringField('Description', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    image_file = StringField('Attachment', validators=[DataRequired()])
    member_id = SelectField(label="Billed to", coerce=int)
    #member_id = SelectField(label="Billed to",coerce=int)
    bill = SubmitField('Add Bill')

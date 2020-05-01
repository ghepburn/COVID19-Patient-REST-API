from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError
from covid19api.models import User
from flask import request
import pandas as pd


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("That Username is taken.  Please choose a different one.")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("That email is taken.  Please choose a different one.")


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')

class PostForm(FlaskForm):
	sex = StringField('Sex', validators=[Length(min=1, max=7)])
	birth_year = IntegerField('Birth Year')
	country = StringField('Country', validators=[Length(max=50)])
	infection_reason = StringField('Infection Reason', validators=[Length(max=50), Optional()])
	confirmed_date = DateField('Date Confirmed')
	deceased_date = DateField('Date Deceased', validators=[Optional()])
	submit = SubmitField('Add')

class UploadForm(FlaskForm):
	file = FileField('File')
	submit=SubmitField('Upload')
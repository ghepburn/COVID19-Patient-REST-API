from Covid19API import db, login_manager, bcrypt
from flask_login import UserMixin
import datetime as dt
import requests

@login_manager.request_loader
def load_user_from_request(request):
	api_key = request.args.get('api_key')
	if api_key:
		hashed_key = bcrypt.generate_password_hash(api_key)
		api_key = Api_Key.query.filter_by(hashed_key=hashed_key).first()
		user = User.query.filter_by(api_key=api_key).first()
		return user
	return None

@login_manager.user_loader
def load_user(user_id):
	return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	api_key = db.relationship('Api_Key', backref='api_key', lazy=True)
	patients = db.relationship('Patient', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"

class Api_Key(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	hashed_key = db.Column(db.String(60), unique=True, nullable=False)
	created = db.Column(db.DateTime(), nullable=False, default=dt.datetime.utcnow())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Patient(db.Model):
	patient_id = db.Column(db.Integer, primary_key=True)
	sex = db.Column(db.String(10))
	birth_year = db.Column(db.String(20))
	country = db.Column(db.String(50))
	infection_reason = db.Column(db.String(150))
	confirmed_date = db.Column(db.DateTime(), nullable=True)
	deceased_date = db.Column(db.DateTime(), nullable = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Patient('{self.patient_id}', sex: '{self.sex}', birth: '{self.birth_year}')"
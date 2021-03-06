from covid19api import db, bcrypt
import datetime as dt


class User(db.Model):
	__table_args__ = {'extend_existing': True}
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	account_type = db.Column(db.Integer, default="Free") 
	role = db.Column(db.String(20), default='Customer')
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	api_key = db.relationship('Api_Key', backref='api_key', lazy=True)
	patients = db.relationship('Patient', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"

	# def get_apikey(self, requested_key):
	# 	for key in self.api_key:
	# 		encrypted_apikey = key.hashed_key
	# 		if bcrypt.check_password_hash(encrypted_apikey, requested_key):
	# 			return key
	# 	return None


class Api_Key(db.Model):
	__table_args__ = {'extend_existing': True}
	id = db.Column(db.Integer, primary_key=True)
	hashed_key = db.Column(db.String(60), unique=True, nullable=False)
	created = db.Column(db.DateTime(), nullable=False, default=dt.datetime.utcnow())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	monthly_call_limit = db.Column(db.Integer, default=3)
	current_call_balance = db.Column(db.Integer, default=3)
	active = db.Column(db.Boolean, default=True)


class Patient(db.Model):
	__table_args__ = {'extend_existing': True}
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
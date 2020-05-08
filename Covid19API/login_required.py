from flask import redirect, url_for, flash, request, session

from .models import Api_Key, User
from covid19api import db, bcrypt

	
def session_authorized():
	if session.get("USERNAME") != None:
		return True
	else:
		return False

def apikey_authorized():
	result = False
	if request.args:
		try:
			username = request.args.get('username')
			provided_api_key = request.args.get('api_key')

			print(f"username: {username}, key: {provided_api_key}")

			user = User.query.filter_by(username=username).first()
			
			print(f"user: {user}")

			for key in user.api_key:
				if bcrypt.check_password_hash(key.hashed_key, provided_api_key):
					api_key = key
			
			print(api_key.active)

			if api_key.active:
				print("its active")
				result = True
				print(f"set result: {result}")

		except:
			return result

	return result


def login_required(func):
	def wrapper(*args, **kwargs):

		if session_authorized() or apikey_authorized():
			x = func(*args, **kwargs)
			return x

		else:
			flash("Please log in.", 'danger')
			return redirect(url_for('login'))
			
	wrapper.__name__ = func.__name__
	return wrapper


def session_required(func):
	def wrapper(*args, **kwargs):

		if session_authorized():
			x = func(*args, **kwargs)
			return x

		else:
			flash("Please log in.", 'danger')
			return redirect(url_for('login'))
			
	wrapper.__name__ = func.__name__
	return wrapper
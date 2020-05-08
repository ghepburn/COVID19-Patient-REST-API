from flask import redirect, url_for, flash, session
from .models import User


def valid_permissions():
	user = User.query.filter_by(username=session["USERNAME"]).first()
	if user.role == "Admin":
		return True
	else:
		return False


def permissions_required(func):
	def wrapper(*args, **kwargs):

		if valid_permissions():
			x = func(*args, **kwargs)
			return x

		else:
			flash("You are not authorized to access.", 'danger')
			return redirect(url_for('home'))
			
	wrapper.__name__ = func.__name__
	return wrapper
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify, make_response
from flask_login import login_user, logout_user, current_user, login_required
import datetime as dt
import secrets
import pandas as pd

from .models import Patient, User, Api_Key
from .forms import RegistrationForm, LoginForm, PostForm, UploadForm
from Covid19API import app, bcrypt, db
from .serializers import PatientSerializer


@app.route('/')
def home():
	return render_template('home.html', title="Covid19API")


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		flash(f"We Got Your Account Created {form.username.data}!", 'success')
		return redirect(url_for('register_success'))
	return render_template('users/registration.html', title="Register", form=form)

@app.route('/register/success')
@login_required
def register_success():
	api_key = secrets.token_hex(16) 
	hashed_api_key = bcrypt.generate_password_hash(api_key).decode('UTF-8')
	key = Api_Key(hashed_key=hashed_api_key, user_id=current_user.id)
	return render_template('users/register_success.html', api_key=api_key)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data): 
			login_user(user)
			flash(f"Hey {current_user.username}!", 'success')
			return redirect(url_for('home'))
		else:
			flash("Login Unsuccessful. Please check username and password", 'danger')
	return render_template('users/login.html', title="Login", form=form) 



@app.route('/logout')
def logout():
	logout_user()
	flash("You are logged out.", 'success')
	return redirect(url_for('home'))


@app.route('/documentation')
def documentation():
	return render_template('documentation.html')


@app.route('/api/patients', methods=['GET', 'POST'])
@login_required
def listPatients():

	form = PostForm()
	
	if form.validate_on_submit():
		patient = Patient(sex=form.sex.data, birth_year=form.birth_year.data, country=form.country.data, infection_reason=form.infection_reason.data, confirmed_date=form.confirmed_date.data, deceased_date=form.deceased_date.data, user_id=current_user.id)
		db.session.add(patient)
		db.session.commit()
		flash('Patient added successfully!', 'success')

	page = request.args.get('page', 1, type=int)
	patients = Patient.query.order_by(Patient.confirmed_date.desc()).paginate(per_page=10, page=page)
	
	return render_template('api/ListPatients.html', patients=patients, form=form)


@app.route('/api/patients/upload', methods=['GET', 'POST'])
def patientUpload():
	form = UploadForm()

	if form.validate_on_submit():
		csv_file = request.files[form.file.name]
		patient_df = pd.read_csv(csv_file)

		correct_columns = ['sex', 'birth_year', 'country', 'infection_reason', 'confirmed_date', 'deceased_date']
		for index, column in enumerate(patient_df.columns):
			if patient_df.columns[index] != correct_columns[index]:
				flash(f"CSV not formatted correctly. See column {index}.")
				return redirect(url_for('patientUpload'))
		for index, patient in patient_df.iterrows():
			confirmed_date = dt.datetime.strptime(str(patient.confirmed_date), "%Y%m%d")
			deceased_date = dt.datetime.strptime(str(patient.deceased_date), "%Y%m%d")
			patient = Patient(sex=patient.sex, birth_year=patient.birth_year, country=patient.country, infection_reason=patient.infection_reason, confirmed_date=confirmed_date, deceased_date=deceased_date, user_id=current_user.id)
			db.session.add(patient)
		db.session.commit()
		flash("CSV file uploaded.  Patients added to database.", "success")
		return redirect(url_for('listPatients'))

	return render_template('api/UploadPatients.html', form=form)


@app.route('/api/patients/patients')
@login_required
def get_all_patients():
	patientList = Patient.query.all()
	patients = []
	serializer = PatientSerializer()
	for patient in patientList:
		patient_json = serializer.dump(patient)
		patients.append(patient_json)

	patients = jsonify({'Patients': patients})

	return patients

@app.route('/api/patients/<int:patient_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def detailPatient(patient_id):
	patient = Patient.query.filter_by(patient_id=patient_id).first()
	if not patient:
		return jsonify({'message': 'no patient found'})

	if request.method=='PUT':
		data = request.get_json()
		patient.sex=data['sex']
		patient.birth_year=int(data['birth_year'])
		patient.country=data['country']
		patient.infection_reason=data['infection_reason']
		patient.confirmed_date=dt.datetime.strptime(data['confirmed_date'], "%Y%m%d")
		patient.deceased_date=deceased_date = dt.datetime.strptime(data['deceased_date'], "%Y%m%d")
		patient.user_id=current_user.id
		db.session.commit()
		return jsonify({'message':'patient edited'})

	if request.method=='DELETE':
		db.session.delete(patient)
		db.session.commit()
		return jsonify({'message':'patient removed'})

	serializer = PatientSerializer()
	patient_json = serializer.dump(patient)
	return patient_json


@app.route('/api/patients/<country>', methods=['GET'])
@login_required
def countryPatient(country):
	patientList = Patient.query.filter_by(country=country)
	patients = []
	serializer = PatientSerializer()
	for patient in patientList:
		patient_json = serializer.dump(patient)
		patients.append(patient_json)
	patients = jsonify({"Patients": patients})
	return patients

@app.route('/api/patients/add', methods=['POST'])
@login_required
def addPatient():
	data = request.get_json()
	confirmed_date = dt.datetime.strptime(data['confirmed_date'], "%Y%m%d")
	deceased_date = dt.datetime.strptime(data['deceased_date'], "%Y%m%d")
	patient = Patient(sex=data['sex'], birth_year=int(data['birth_year']), country=data['country'], infection_reason=data['infection_reason'], confirmed_date=confirmed_date, deceased_date=deceased_date, user_id=current_user.id)
	db.session.add(patient)
	db.session.commit()
	return jsonify({'message': 'new patient created'})

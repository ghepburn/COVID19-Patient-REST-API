from marshmallow import Schema, fields

class PatientSerializer(Schema):
	patient_id = fields.Str()
	sex = fields.Str()
	birth_year = fields.Integer()
	country = fields.Str()
	infection_reason = fields.Str()
	confirmed_date = fields.DateTime()
	deceased_date = fields.DateTime()
	user_id = fields.Integer()
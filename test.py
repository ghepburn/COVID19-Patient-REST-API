from covid19api.models import User

Greg = User.query.all()[-1]

Greg.valid_apikey("12345")
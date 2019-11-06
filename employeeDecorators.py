
from functools import wraps
from datetime import date
from flask import request
from flask import abort
from flaskServer.models import db, positions, Employee, teams

def calc_age(birth_day):
	today = date.today()
	birth_helper = birth_day.split('-')

	b_day = int(birth_helper[0])
	b_month = int(birth_helper[1])
	b_year = int(birth_helper[2])
	#calc and return the age.
	return today.year - b_year - ((today.month, today.day) < (b_month, b_day))



def verify_employee(f):
	@wraps(f)
	def decorated_view(*args, **kwargs):
		# validate json data.
		json_data = request.get_json()
		if "full_name" not in json_data or "birth_day" not in json_data:
			print("json fields missing")
			abort(405, error='invalid JSON stracture.')
		# verify full anme length is below 50 characters.

		full_name = json_data.get('full_name')
		name_len = len(str(full_name))
		if name_len >= 50:
			print("Name is to long.")
			abort(405, error='invalid characters length for full_name.')

		# second, check if employee is below 18 years old
		birth_day = json_data.get('birth_day')
		age = calc_age(birth_day)
		if age < 18:
			print("age is below 18.")
			abort(405, 'illegal employee age: {0}.'.format(age))

		return f(*args, **kwargs)
	return decorated_view



def verify_positions_in_db(f):
	@wraps(f)
	def decorated_view(*args, **kwargs):
		# validate the above positions exist: employee, team_leader, ceo, cto
		pos_to_find = {
			'employee': False,
			'team_leader': False,
			'CEO': False,
			'CTO': False
		}
		# get all positions form db, and find if one not exist
		current_positions = db.session.query(positions).all()
		for pos in current_positions:
			print('found position {0}'.format(pos.position_name))
			if pos.position_name in pos_to_find:
				pos_to_find[pos.position_name] = True

		for attr, value in pos_to_find.items():
			if value == False:
				# if found position that not exist, add to db
				print('value: {0} of key: {1}'.format(value, attr))
				print('About to carete position: {0}'.format(attr))
				db.session.add(positions(position_name=attr))
		return f(*args, **kwargs)
	return decorated_view



def verify_employee_exist(f):
	@wraps(f)
	def decorated_view(*args, **kwargs):
		# check if current employee exist in db
		json_data = request.get_json()
		full_name = json_data['employee_name']
		emp = Employee.query.filter_by(full_name=full_name).first()
		if emp == None:
			abort(405)

		return f(*args, **kwargs)
	return decorated_view


def verify_team_exist(f):
	@wraps(f)
	def decorated_view(*args, **kwargs):
		#check if current team exist in db
		json_data = request.get_json()
		team_name = json_data['team_name']
		team = teams.query.filter_by(team_name=team_name).first()
		if team == None:
			abort(405)

		return f(*args, **kwargs)
	return decorated_view




















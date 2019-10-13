import requests
import json
from flaskServer import app
from flaskServer.employeeDecorators import verify_employee, verify_positions_in_db, verify_employee_exist, verify_team_exist
from flaskServer.models import Employee, positions, db, position_of_employee, employees_in_teams, teams, locations
from datetime import datetime
from flask import request, abort, render_template, send_from_directory, make_response, jsonify
from sqlalchemy import func

@app.route('/')
def default_route():
	return str(datetime.now()) + '\n'

@app.route('/test')
def test_route():
	return 'Hello World, I a\'m Flask!\n'

@app.route('/create/employee', methods=["POST"])
@verify_positions_in_db
@verify_employee
def create_employee():
	# create new employee.
	json_data = request.get_json()
	full_name = json_data['full_name']
	birth_day = json_data['birth_day']
	email = json_data['email']
	salary_usd = json_data['salary_usd']
	first_work_day = json_data['first_work_day']

	# check if such employee does not exist.
	find_emp_in_db = Employee.query.filter_by(full_name=full_name).first()
	if not find_emp_in_db == None:
		abort(405)
	# create new Employee object.
	new_employee = Employee(full_name=full_name, 
				birth_day=birth_day, email=email,
				salary_usd=salary_usd, first_work_day=first_work_day)
	# add to db.
	db.session.add(new_employee)
	db.session.commit()
	# set default role: employee
	tmp_emp = Employee.query.filter_by(full_name=full_name).first()
	tmp_pos = positions.query.filter_by(position_name='employee').first()
	new_emp_pos = position_of_employee(position_id=tmp_pos.position_id,
						employee_id=tmp_emp.employee_id) 
	# commit changes to db.
	db.session.add(new_emp_pos)
	db.session.commit()
	return "new user created!\n"


@app.route('/update/employee', methods=['POST'])
@verify_employee
def update_employee():
	json_data = request.get_json()
	full_name = json_data['full_name']
	birth_day = json_data['birth_day']
	email = json_data['email']
	salary_usd = json_data['salary_usd']
	first_work_day = json_data['first_work_day']

	# get the employee from db by full_name.
	employee_from_db = Employee.query.filter_by(full_name=full_name).first()
	if not employee_from_db.full_name == full_name:
		abort(405)
	# update employee details.
	employee_from_db.birth_day = birth_day
	employee_from_db.email = email
	employee_from_db.salary_usd = salary_usd
	employee_from_db.first_work_day = first_work_day
	# commit changes to db.
	db.session.commit()
	return 'employee {0} updated.\n'.format(full_name)



@app.route('/create/team', methods=['POST'])
def create_team():
	json_data = request.get_json()
	team_name = json_data['team_name']

	# check if team already exists.
	tmp_team = teams.query.filter_by(team_name=team_name).first()
	if not tmp_team == None:
		print("team {0} already exist.".format(team_name))
		abort(405)
	# create team.
	new_team = teams(team_name=team_name)
	db.session.add(new_team)
	db.session.commit()
	return 'team {0} created!\n'.format(team_name)



@app.route('/assign', methods=['POST'])
@verify_employee_exist
@verify_team_exist
def assign_employee_to_team():
	json_data = request.get_json()
	employee_name = json_data['employee_name']
	team_name = json_data['team_name']

	# get ids of employee & team
	tmp_employee = Employee.query.filter_by(full_name=employee_name).first()
	tmp_team = teams.query.filter_by(team_name=team_name).first()
	# remove old assignments if needed
	old_assignment = employees_in_teams.query.filter_by(employee_id=tmp_employee.employee_id).first()
	if not old_assignment == None:
		db.session.delete(old_assignment)
	# create assignment
	new_assign = employees_in_teams(employee_id=tmp_employee.employee_id,
					team_id=tmp_team.team_id)
	db.session.add(new_assign)
	db.session.commit()
	return 'employee {0} was assigned to group {1}\n'.format(employee_name, team_name)
	


@app.route('/remove/employee', methods=['POST'])
@verify_employee_exist
def remove_employee():
	json_data = request.get_json()
	employee_name = json_data['employee_name']
	# get the employee from db
	employee_to_rem = Employee.query.filter_by(full_name=employee_name).first()
	# remove all employees relationsheeps
	
	# remove records of positions
	employee_positions = position_of_employee.query.filter_by(employee_id=employee_to_rem.employee_id)
	for employee_pos in employee_positions:
		db.session.delete(employee_pos)

	# remove records of team assignments
	employee_teams = employees_in_teams.query.filter_by(employee_id=employee_to_rem.employee_id)
	for employee_in_team in employee_teams:
		db.session.delete(employee_in_team)

	# remove locations
	employee_location = locations.query.filter_by(employee_id=employee_to_rem.employee_id)
	for location in employee_location:
		db.session.delete(location)

	# remove the employee
	db.session.delete(employee_to_rem)
	db.session.commit()
	return 'employee {0} removed\n.'.format(employee_name)


@app.route('/remove/team', methods=['POST'])
@verify_team_exist
def remove_team():
	json_data = request.get_json()
	team_name = json_data['team_name']
	# get the team from db
	team_to_rem = teams.query.filter_by(team_name=team_name).first()
	# remove all team relationsheep
	
	# remove records of employee assignments
	employee_teams = employees_in_teams.query.filter_by(team_id=team_to_rem.team_id)
	for employee_in_team in employee_teams:
		db.session.delete(employee_in_team)

	# remove the team
	db.session.delete(team_to_rem)
	db.session.commit()
	return 'team {0} was removed.\n'.format(team_name)



@app.route('/set/location', methods=['POST'])
@verify_employee_exist
def set_employee_location():
	json_data = request.get_json()
	longitude = json_data['longitude']
	latitude = json_data['latitude']
	employee_name = json_data['employee_name']
	# get the employee
	employee_in_db = Employee.query.filter_by(full_name=employee_name).first()
	# get employee location
	employee_location = locations.query.filter_by(employee_id=employee_in_db.employee_id).first()

	if not employee_location == None:
		#update
		employee_location.location_latitude = latitude
		employee_location.location_longitude = longitude
	else:
		#create new location
		new_location = locations(employee_id=employee_in_db.employee_id,
						location_latitude=latitude,
						location_longitude=longitude)
		db.session.add(new_location)
	db.session.commit()
	return 'employee {0} location was set.\n'.format(employee_name)


@app.route('/set/role', methods=['POST'])
@verify_employee_exist
def set_employee_role():
	json_data = request.get_json()
	employee_name = json_data['employee_name']
	new_role = json_data['role']
	# get the employee
	employee_in_db = Employee.query.filter_by(full_name=employee_name).first()
	# get current role
	employee_role = position_of_employee.query.filter_by(employee_id=employee_in_db.employee_id).first()
	# get desired role id
	desired_role = positions.query.filter_by(position_name=new_role).first()

	# update the role if needed
	employee_role.position_id = desired_role.position_id
	db.session.commit()
	return 'employee {0} role was set to {1}\n'.format(employee_name, new_role)



########## GET REQUESTS HANDLERS ##########

@app.route('/get/all/teams', methods=['GET'])
def get_all_groups():
	all_teams = db.session.query(teams).all()
	resp = {'data': []}
	for team in all_teams:
		count = db.session.query(func.count(employees_in_teams.team_id).filter(employees_in_teams.team_id == team.team_id)).scalar()
		print('HERE I AM: ' + str(count))
		resp['data'].append({'team_name': team.team_name, 'members': count})
	return jsonify(resp)


@app.route('/get/all/employees', methods=['GET'])
def get_all_employees_with_all_details():
	employees = Employee.query.all()
	resp = {'data': []}
	for employee in employees:
		resp['data'].append(employee.to_object())
	return jsonify(resp)


@app.route('/get/employee/<full_name>', methods=['GET'])
def get_employee_by_name_with_details(full_name):
	employee = Employee.query.filter_by(full_name=full_name).first()
	return jsonify(employee.to_object())


@app.route('/get/all/employeesRoles', methods=['GET'])
def get_all_employees_roles():
	details_from_db = db.session.query(Employee, position_of_employee, positions).filter(Employee.employee_id == position_of_employee.employee_id).filter(position_of_employee.position_id == positions.position_id).all()

	result = {'data': []}
	for emp, assign, pos in details_from_db:
		result['data'].append({'full_name': emp.full_name, 'salary_usd': emp.salary_usd, 'birth_day': emp.birth_day, 'e_mail': emp.email, 'first_work_day': emp.first_work_day, 'role': pos.position_name})

	return jsonify(result)


@app.route('/get/all/employeesWithGroups', methods=['GET'])
def get_all_employees_groups():
	details_from_db = db.session.query(Employee, position_of_employee, positions, employees_in_teams, teams).filter(Employee.employee_id == position_of_employee.employee_id).filter(position_of_employee.position_id == positions.position_id).filter(Employee.employee_id == employees_in_teams.employee_id).filter(employees_in_teams.team_id == teams.team_id).all()

	result = {'data': []}
	for emp, assign, pos, team_assign, team in details_from_db:
		result['data'].append({'full_name': emp.full_name, 'salary_usd':emp.salary_usd ,'birth_day': emp.birth_day, 'e_mail': emp.email, 'first_work_day': emp.first_work_day, 'role': pos.position_name, 'team_name': team.team_name})

	return jsonify(result)


########### GET Frontend ##############

# serve required js files
@app.route('/js/<path:path>', methods=['GET'])
def send_js(path):
	return send_from_directory(app.static_folder, path)

# serve angularJS app
@app.route('/apolloShield', methods=['GET'])
def get_frontend_app():
	return render_template('index.html')

@app.route('/getEURsalary', methods=['GET'])
def get_eur_salary():
	eur_val_raw = requests.get('https://free.currconv.com/api/v7/convert?q=USD_EUR&compact=ultra&apiKey=75b825886c5adacdcc78')
	eur_val_data = str(eur_val_raw.content.decode("utf-8"))
	print(eur_val_data)
	eur_val_j = json.loads(eur_val_data)
	eur_val = eur_val_j['USD_EUR']
	print(eur_val)
	
	details_from_db = db.session.query(Employee, position_of_employee, positions, employees_in_teams, teams).filter(Employee.employee_id == position_of_employee.employee_id).filter(position_of_employee.position_id == positions.position_id).filter(Employee.employee_id == employees_in_teams.employee_id).filter(employees_in_teams.team_id == teams.team_id).all()

	result = {'data': []}
	for emp, assign, pos, team_assign, team in details_from_db:
		eur_salaty = float(emp.salary_usd) * float(eur_val)
		print(emp.salary_usd)
		print(str(eur_salaty))
		result['data'].append({'full_name': emp.full_name, 'salary_usd': str(eur_salaty) ,'birth_day': emp.birth_day, 'e_mail': emp.email, 'first_work_day': emp.first_work_day, 'role': pos.position_name, 'team_name': team.team_name})

	return jsonify(result)



	

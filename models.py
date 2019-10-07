
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

db_config = {
	'postgres_url': '127.0.0.1:5432',
	'postgres_user': 'postgres',
	'postgres_passw': '123456',
	'postgress_db': 'apollo_employees'
}

db_url = 'postgresql+psycopg2://{user}:{passw}@{url}/{db}'.format(user=db_config['postgres_user'], passw=db_config['postgres_passw'], url=db_config['postgres_url'], db=db_config['postgress_db'])


class Employee(db.Model):
	# model for employee table
	__tablename__ = 'employees'

	employee_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
	full_name = db.Column(db.String(51), index=False, unique=True, nullable=False)
	birth_day = db.Column(db.String(12), index=False, unique=False, nullable=False)
	email = db.Column(db.String(100), index=False, unique=False, nullable=False)
	first_work_day = db.Column(db.String(10), index=False, unique=False, nullable=False)
	salary_usd = db.Column(db.String(200), index=False, unique=False, nullable=False)
	
	def to_object(self):
		return {
			'full_name': self.full_name,
			'birth_day': self.birth_day,
			'email': self.email,
			'first_work_day': self.first_work_day,
			'salary_usd': self.salary_usd
			}

	def __repr__(self):
		return '{\'full_name\': \'{0}\', \'birth_day\': \'{1}\', \'email\': \'{2}\', \'salary\': \'{3}\', \'first_work_day\': \'{4}}\''.format(self.full_name, self.birth_day, self.email, self.salary_usd, self.first_work_day)


class teams(db.Model):
	# model for teams table
	__tablename__ = 'teams'
	team_id=db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
	team_name=db.Column(db.String(51), index=False, unique=True, nullable=False)

	def to_object(self):
		return {'team_name': self.team_name}

	def __repr__(self):
		return '{team_name: {0}}'.format(self.team_name)

class locations(db.Model):
	# model for locations table
	__tablename__ = 'locations'
	
	location_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
	employee_id = db.Column(db.Integer, unique=True, nullable=False)
	location_latitude = db.Column(db.String(100), index=False, unique=False, nullable=False)
	location_longitude = db.Column(db.String(100), index=False, unique=False, nullable=False)

	def __repr__(self):
		return '<location, user: {0} at lat: {1}, lon: {2}>'.format(self.employee_id, self.location_latitude, self.location_longitude)

class employees_in_teams(db.Model):
	# model for employees to teams relationsheep table
	__tablename__ = 'employees_in_teams'
	
	relation_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
	employee_id = db.Column(db.Integer, unique=False, nullable=False)
	team_id = db.Column(db.Integer, unique=False, nullable=False)

	def __repr__(self):
		return '{employee_id: {0}, team_id: {1}}'.format(self.employee_id, self.relation_id)

class positions(db.Model):
	# model for employees positions
	__tablename__ = 'employee_positions'
	
	position_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
	position_name = db.Column(db.String(51), index=False, unique=True, nullable=False)

	def __repr__(self):
		return '{position: {0}}'.format(self.position_name)


class position_of_employee(db.Model):
	# model for positions of employees
	__tablename__ = 'positions_of_employees'
	
	employee_position_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
	employee_id = db.Column(db.Integer, unique=False, nullable=False)
	position_id = db.Column(db.Integer, unique=False, nullable=False)

	def __repr__(self):
		return '{employee_id: {0}, position_id: {1}}'.format(self.employee_id, self.position_id)

class hr_notes(db.Model):
	# hr notes for employees
	__tablename__ = 'hr_notes_for_employees'

	note_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
	employee_id = db.Column(db.String(51), index=False, unique=True, nullable=False)
	date_of_note = db.Column(db.String(51), index=False, unique=True, nullable=False)
	note_text = db.Column(db.String(255), index=False, unique=True, nullable=False)

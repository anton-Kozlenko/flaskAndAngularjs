### !!! IMPORTANT !!! ###
employees birth dates must be set as : "dd-mm-yyyy".

### global info ###

This app is using postgreSQL to save it's data.
all queries to db are wraped with SQLAlchemy.
every important api endpoint on the server is protected by a decorator.
external api usage to get value of eur by usd - api token can be seen in the code.
external api usage of Google maps.
employees locations are generated when employees are created.

### Backend instructions ###

postgreSQL must be set to suite the configuration in 'models.py' file.
all dependencies must be installed (Flask, SQLAlchemy...).
setup environment variable 'FLASK_APP' to 'app.py' with absolute path using 'EXPORT'.
run 'flask run --host=0.0.0.0'

### Frontend instructions ###

set your servers ip address in files 'index.html' and 'groupsController.js'.
can be easily done with 'sed': "sed -i 's/{curr_ip}/{your_ip}/g' fileName"
!! do it before running the server !!

### application usage instructions ###

there are 4 components in the application
1. controlling view of salary: usd/uer
2. table with teams
3. table with employees
4. Google map

1. just use the radio button when viewing employees

2. there is a default team 'all employees', its not an actual team, just a list of all employees - can't add employees to this team - because it's not.
   you can create teams - one at a time, using suitable button below.
   click on radio button near a team name will show its members on the next to table.
   you can delete selected team with suitable button.

3. when team is selected you will see its members and theit details in this table.
   you can create new employees, and they will be added to the selected team.
   you can delete employees, and update their details (not everything) - YOU WILL GET 405 ERRORR if you will try to add employee with age under 18.
   you can click on employees name, and his/her location will be shown on the map below.

4. this map will initialize on app load, employees locations will bw shown when clicked.

### api tests ###

create employee
 curl -d '{"full_name": "{name}", "birth_day": "{dd-mm-yyyy}", "email": "{mail}", "salary_usd": "{salary}", "first_work_day": "{day}"}' -H "Content-Type: application/json" -X POST "http://{ip address}:5000/create/employee"
 
update employee
 curl -d '{"full_name": "{name}", "birth_day": "{dd-mm-yyyy}", "email": "{mail}", "salary_usd": "{salary}", "first_work_day": "{day}"}' -H "Content-Type: application/json" -X POST "http://{ip address}:5000/update/employee"

 remove employee
 curl -d '{"employee_name": "{name}"}' -H "Content-Type: application/json" -X POST "http://{ip address}:5000/remove/employee"
 
 create team
 curl -d '{"team_name": "{team}"}' -H "Content-Type: application/json" -X POST "http://{ip address}:5000/create/team"
 
 remove team
 curl -d '{"team_name": "{team}"}' -H "Content-Type: application/json" -X POST "http://{ip address}:5000/remove/team"
 
 assign employee to team
 curl -d '{"employee_name": "{name}", "team_name": "{team}"}' -H "Content-Type: application/json" -X POST "http://{ip address}:5000/assign"
 
 set role
 curl -d '{"employee_name": "{name}", "role": "{role}"}' -H "Content-Type: application/json" -X POST "http://{ip address}:5000/set/role"
 
 set location
 curl -d '{"employee_name": "{name}", "longitude": "{lon}", "latitude": "{lat}"}' -H "Content-Type: application/json" -X POST "http://{ip address}:5000/set/location"
 

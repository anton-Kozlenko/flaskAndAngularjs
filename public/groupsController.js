
var groupsApp = angular.module('groupsApp', []);


groupsApp.config(['$interpolateProvider', function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
  	$interpolateProvider.endSymbol(']]');
}]);


groupsApp.controller('ctrlGroups', function($scope, $http) {

	$scope.newTeamToCreate = '';
	$scope.daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'];
	$scope.empRoles = ['team_leader', 'CTO', 'CEO', 'employee'];

	$scope.updateData = function() {
		$http.get('http://10.0.0.5:5000/get/all/employeesRoles')
        	.then(function(response) {
                	var res_j = response.data;
                	$scope.allEmployees = res_j['data'];
                	$scope.total_employees = $scope.allEmployees.length
        	});

		$http.get('http://10.0.0.5:5000/get/all/employeesWithGroups')
        	.then(function(response) {
                	var res_j = response.data;
                	$scope.allEmployeesGroups = res_j['data'];
        	});

		$http.get('http://10.0.0.5:5000/getEURsalary')
                .then(function(response) {
                        var res_j = response.data;
                        $scope.allEmployeesGroupsEUR = res_j['data'];
                });

		$http.get('http://10.0.0.5:5000/get/all/teams')
        	.then(function(response) {
                	var res_j = response.data;
                	$scope.teamsList = res_j['data'];
		});
	};


	$http.get('http://10.0.0.5:5000/get/all/employeesRoles')
	.then(function(response) {
		var res_j = response.data;
		$scope.allEmployees = res_j['data'];
		$scope.total_employees = $scope.allEmployees.length
	});

	$http.get('http://10.0.0.5:5000/get/all/employeesWithGroups')
	.then(function(response) {
		var res_j = response.data;
		$scope.allEmployeesGroups = res_j['data'];
	});

	$http.get('http://10.0.0.5:5000/get/all/teams')
	.then(function(response) {
		var res_j = response.data;
		$scope.teamsList = res_j['data'];
		//$scope.total_employees = 0;
		//angular.forEach($scope.teamsList, function(obj){
		//	$scope.total_employees += Number(obj.members);
		//});
	});

	$scope.newEmployeeMode = false;
	$scope.selectedEmployee = '';	

	$scope.employeeClickTrigger = function(input) {
		$scope.selectedEmployee = input;
	}

	$scope.addEmployee = function() {
		if ($scope.newEmployeeMode || $scope.selectedGroup == '' || $scope.selectedGroup == 'all') {
			return;
		}
		$scope.newEmployeeMode = true;
		$scope.addEmployeeElement = {'full_name': '', 'birth_day': '', 'e_mail': '', 'salary_usd': '', 'first_work_day': '', 'role': ''};
		
	};

	$scope.saveNewEmployee = function() {
		if ($scope.newEmployeeMode) {
			if ($scope.selectedGroup == '' || $scope.selectedGroup == 'all') {
				alert('Specific team should be selected.');
				return;
			}
			if ($scope.addEmployeeElement.full_name == '') {
				alert('Enter full name.');
				return;
			}
			if ($scope.addEmployeeElement.birth_day == '') {
				alert('enter birth date.');
                	        return;
			}
			if ($scope.addEmployeeElement.e_mail == '') {
				alert('enter Email.');
				return;
			}
			if (Number.isFinite(Number($scope.addEmployeeElement.salary_usd)) == false) {
				alert('enter salary number in usd.');
				return;
			}
			if ($scope.addEmployeeElement.first_work_day == '') {
				alert('select First work day.');
				return;
			}
			if ($scope.addEmployeeElement.role == '') {
				alert('select role.');
				return;
			}

			var data = {
				"full_name": $scope.addEmployeeElement.full_name,
				"birth_day": $scope.addEmployeeElement.birth_day,
				"email": $scope.addEmployeeElement.e_mail,
				"salary_usd": $scope.addEmployeeElement.salary_usd,
				"first_work_day": $scope.addEmployeeElement.first_work_day
			};
			 // create employee
			$http.post('http://10.0.0.5:5000/create/employee', data,{'Content-Type': 'application/json'})
			.then(function(response) {
				data = {"employee_name": $scope.addEmployeeElement.full_name, "role": $scope.addEmployeeElement.role};
				// role assignment
				$http.post('http://10.0.0.5:5000/set/role', data,{'Content-Type': 'application/json'})
				.then(function(response) {
					data = {"employee_name": $scope.addEmployeeElement.full_name, "team_name": $scope.selectedGroup};
					// group assignment
					$http.post('http://10.0.0.5:5000/assign', data,{'Content-Type': 'application/json'})
					.then(function(response) {
						$scope.addEmployeeElement = {'full_name': '', 'birth_day': '', 'e_mail': '', 'salary_usd': '', 'first_work_day': '', 'role': ''};
						$scope.newEmployeeMode = false;
						$http.get('http://10.0.0.5:5000/get/all/employeesWithGroups')
						.then(function(response) {
							var res_j = response.data;
							$scope.allEmployeesGroups = res_j['data'];
							$scope.teamClickTrigger($scope.selectedGroup);
							$scope.updateData();
                                        	});
                                	});
                        	});
                	});
			
		}
		else if ($scope.updateEmployeeMode) {
		
		
			var data = {
				"full_name": $scope.employeeToUpdate.full_name,
				"birth_day": $scope.employeeToUpdate.birth_day,
				"email": $scope.employeeToUpdate.e_mail,
				"salary_usd": $scope.employeeToUpdate.salary_usd,
				"first_work_day": $scope.employeeToUpdate.first_work_day
			};
			// update employee
                	$http.post('http://10.0.0.5:5000/update/employee', data,{'Content-Type': 'application/json'})
                	.then(function(response) {
                        	data = {"employee_name": $scope.employeeToUpdate.full_name, "role": $scope.employeeToUpdate.role};
				// role assignment
				$http.post('http://10.0.0.5:5000/set/role', data,{'Content-Type': 'application/json'})
                		.then(function(response) {
					$http.get('http://10.0.0.5:5000/get/all/employeesWithGroups')
					.then(function(response) {
						var res_j = response.data;
						$scope.allEmployeesGroups = res_j['data'];
						$scope.updateEmployeeMode = false;
						$scope.teamClickTrigger($scope.selectedGroup);
						$scope.updateData();
					});
					//$http.get('http://10.0.0.5:5000/getEURsalary')
                			//.then(function(response) {
                        		//	var res_j = response.data;
                        		//	$scope.allEmployeesGroupsEUR = res_j['data'];
                			//});
               			});
                	});
		}
	};

	$scope.removeEmployee = function() {
		if ($scope.selectedEmployee == '') {
			alert('none employee is selected.');
			return;
		}
		data = {"employee_name": $scope.selectedEmployee.full_name};
		$http.post('http://10.0.0.5:5000/remove/employee', data,{'Content-Type': 'application/json'})
		.then(function(response) {
			$scope.selectedEmployee == ''
			$http.get('http://10.0.0.5:5000/get/all/employeesWithGroups')
			.then(function(response) {
				var res_j = response.data;
				$scope.allEmployeesGroups = res_j['data'];
				$scope.teamClickTrigger($scope.selectedGroup);
				$scope.updateData();
			});
			//$http.get('http://10.0.0.5:5000/getEURsalary')
                	//.then(function(response) {
                        //	var res_j = response.data;
                        //	$scope.allEmployeesGroupsEUR = res_j['data'];
                	//});
		});
	};


	$scope.coinType = 'usd';

	$scope.displaySalary = function(input) {
		if (input === 'eur') {
			$scope.coinType = 'eur';
			$http.get('http://10.0.0.5:5000/getEURsalary')
                        .then(function(response) {
                                var res_j = response.data;
                                $scope.allEmployeesGroups = res_j['data'];
				$scope.teamClickTrigger($scope.selectedGroup);
                        });
		}
		else {
			$scope.coinType = 'usd';
			$http.get('http://10.0.0.5:5000/get/all/employeesWithGroups')
                        .then(function(response) {
                                var res_j = response.data;
                                $scope.allEmployeesGroups = res_j['data'];
				$scope.teamClickTrigger($scope.selectedGroup);
                        });
		}
	}


	$scope.updateEmployeeMode = false;
	$scope.updateEmployee = function() {
		if ($scope.selectedEmployee == '' || $scope.newEmployeeMode || $scope.updateEmployeeMode) {
                        alert('none employee is selected or prev procedure not finished.');
                        return;
                }
		var index;
		for(var iter in $scope.selectedTeamMembers) {
			if ($scope.selectedTeamMembers[iter].full_name === $scope.selectedEmployee.full_name) {
				$scope.employeeToUpdate = $scope.selectedTeamMembers[iter];
				index = iter;
				break;
				alert('found emp to update:' + JSON.stringify($scope.employeeToUpdate));
			}
		}
		$scope.selectedTeamMembers.splice(index, 1);
		$scope.updateEmployeeMode = true;
	};


	$scope.selectedGroup = '';
	$scope.selectedTeamMembers = [];
	$scope.newGroupMode = false;

	$scope.addGroup = function() {
		if ($scope.newGroupMode) {
			return;
		}
		$scope.newGroupMode = true;
		$scope.addGroupElement = [{'team_name': '', 'members': ''}];
	};

	$scope.saveNewGroup = function() {
		console.log(document.getElementById("newTeam"));
		input = document.getElementById("newTeam").value;
		alert('saving group: '+ input)
		if($scope.newGroupName == '') {
			alert('input is empty...')
			return;
		}
		var data = {'team_name': input};
		$http.post('http://10.0.0.5:5000/create/team', data,{'Content-Type': 'application/json'})
		.then(function(response) {
			$scope.addGroupElement = [];
			$scope.updateData();
		});
		$scope.newGroupMode = false;
	};
	
	$scope.removeTeam = function() {
		if ($scope.newGroupMode || $scope.selectedGroup == '' || $scope.selectedGroup == 'all') {
			alert('choose team to remove');
			return;
		}
		var data = {'team_name': $scope.selectedGroup};
		 $http.post('http://10.0.0.5:5000/remove/team', data,{'Content-Type': 'application/json'})
                .then(function(response) {
                        $scope.addGroupElement = [];
                        $scope.updateData();
                });
	}

	$scope.teamClickTrigger = function(input) {
		$scope.selectedGroup = input;
		$scope.selectedTeamMembers = [];

		if (input == 'all'){
			$scope.selectedTeamMembers = $scope.allEmployees
		}
		else {
			angular.forEach($scope.allEmployeesGroups, function(obj){
				if(obj.team_name == $scope.selectedGroup) {
					$scope.selectedTeamMembers.push(obj);
				}
			});
		}
	};
});

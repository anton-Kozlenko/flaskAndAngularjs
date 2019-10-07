
var groupsApp = angular.module('groupsApp', []);

groupsApp.controller('ctrlGroups', function($scope, $http) {

	$scope.newTeamToCreate = 'Anton';

	$scope.updateData = function() {
		$http.get('http://192.168.43.129:5000/get/all/employeesRoles')
        	.then(function(response) {
                	var res_j = response.data;
                	$scope.allEmployees = res_j['data'];
                	$scope.total_employees = $scope.allEmployees.length
        	});

		$http.get('http://192.168.43.129:5000/get/all/employeesWithGroups')
        	.then(function(response) {
                	var res_j = response.data;
                	$scope.allEmployeesGroups = res_j['data'];
        	});

		$http.get('http://192.168.43.129:5000/get/all/teams')
        	.then(function(response) {
                	var res_j = response.data;
                	$scope.teamsList = res_j['data'];
		});
	};


	$http.get('http://192.168.43.129:5000/get/all/employeesRoles')
	.then(function(response) {
		var res_j = response.data;
		$scope.allEmployees = res_j['data'];
		$scope.total_employees = $scope.allEmployees.length
	});

	$http.get('http://192.168.43.129:5000/get/all/employeesWithGroups')
	.then(function(response) {
		var res_j = response.data;
		$scope.allEmployeesGroups = res_j['data'];
	});

	$http.get('http://192.168.43.129:5000/get/all/teams')
	.then(function(response) {
		var res_j = response.data;
		$scope.teamsList = res_j['data'];
		//$scope.total_employees = 0;
		//angular.forEach($scope.teamsList, function(obj){
		//	$scope.total_employees += Number(obj.members);
		//});
	});

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

	$scope.saveNewGroup = function(input) {
		alert('saving group: '+ input)
		if($scope.newGroupName == '') {
			alert('input is empty...')
			return;
		}
		var data = {'team_name': input};
		$http.post('http://192.168.43.129:5000/create/team', data,{'Content-Type': 'application/json'})
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
		 $http.post('http://192.168.43.129:5000/remove/team', data,{'Content-Type': 'application/json'})
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

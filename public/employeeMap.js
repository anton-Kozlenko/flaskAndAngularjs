
var cities = [{
	city: 'India',
	desc: 'The Indian economy is the worlds seventh-largest by nominal GDP and third-largest by purchasing power parity (PPP).',
	lat: 23.200000,
	long: 79.225487
	}, {
  city: 'New Delhi',
  desc: 'Delhi, officially the National Capital Territory of Delhi, is the Capital territory of India. It has a population of about 11 million and a metropolitan population of about 16.3 million',
  lat: 28.500000,
  long: 77.250000
}, {
  city: 'Mumbai',
  desc: 'Mumbai, formerly called Bombay, is a sprawling, densely populated city on India’s west coast',
  lat: 19.000000,
  long: 72.90000
}, {
  city: 'Kolkata',
  desc: 'Kolkata is the capital of the Indian state of West Bengal. It is also the commercial capital of East India, located on the east bank of the Hooghly River',
  lat: 22.500000,
  long: 88.400000
}, {
  city: 'Chennai	',
  desc: 'Chennai holds the colonial past and is an important city of South India. It was previously known as Madras',
  lat: 13.000000,
  long: 80.250000
}, {
  city: 'Gorakhpur',
  desc: 'Gorakhpur also known as Gorakhshpur is a city along the banks of Rapti river in the eastern part of the state of Uttar Pradesh in India, near the Nepal border 273 east of the state capital Lucknow',
  lat: 26.7588,
  long: 83.3697
}];

//Create angular controller.
var mapApp = angular.module('mapApp', []);
mapApp.controller('ctrlMap', function($scope) {
  $scope.highlighters = [];
  $scope.gMap = null;
  
  var winInfo = new google.maps.InfoWindow();
  
  var googleMapOption = {
    zoom: 4,
    center: new google.maps.LatLng(25, 80),
    mapTypeId: google.maps.MapTypeId.TERRAIN
  };

  $scope.gMap = new google.maps.Map(document.getElementById('map'), googleMapOption);

  

  var createHighlighter = function(citi) {

    var citiesInfo = new google.maps.Marker({
      map: $scope.gMap,
      position: new google.maps.LatLng(citi.lat, citi.long),
      title: citi.city
    });

    citiesInfo.content = '<div>' + citi.desc + '</div>';

    google.maps.event.addListener(citiesInfo, 'click', function() {
      winInfo.setContent('<h1>' + citiesInfo.title + '</h1>' + citiesInfo.content);
      winInfo.open($scope.gMap, citiesInfo);
    });
    $scope.highlighters.push(citiesInfo);
  };

  for (i = 0; i < cities.length; i++) {
    createHighlighter(cities[i]);
  }

});

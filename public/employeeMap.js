var module = angular.module('leafletMap', []);
module.directive('sap', function() {
    return {
        restrict: 'E',
        replace: true,
        template: '<div></div>',
        link: function(scope, element, attrs) {
            var map = L.map(attrs.id, {
                center: [40, -86],
                zoom: 10
            });
            //create a CloudMade tile layer and add it to the map
            L.tileLayer('http://{s}.tile.cloudmade.com/57cbb6ca8cac418dbb1a402586df4528/997/256/{z}/{x}/{y}.png', {
                maxZoom: 18
            }).addTo(map);

            //add markers dynamically
            var points = [{lat: 40, lng: -86},{lat: 40.1, lng: -86.2}];
            for (var p in points) {
                L.marker([points[p].lat, points[p].lng]).addTo(map);
            }
        }
    };
});

function MapCtrl($scope) {}

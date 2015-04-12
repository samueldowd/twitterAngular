var myApp = angular.module('myApp', []);

myApp.controller('MyController', ['$scope', '$http', function($scope, $http) {
  $http.get('js/tweets.json').success(function(data) {
    $scope.tweets = data;
  });
}]);


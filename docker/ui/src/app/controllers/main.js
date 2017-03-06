/**
 * @ngdoc function
 * @name autoscienceApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the autoscienceApp
 */

app.controller('mainCtrl', function ($scope, $http) {
  $http({
      method: 'GET',
      url: '/cog/datasets'
    }).then(function successCallback(response) {
      // this callback will be called asynchronously
      // when the response is available
      $scope.datasets = response.data;
      console.log(response.data);
    }, function errorCallback(response) {
      // called asynchronously if an error occurs
      // or server returns response with an error status.
    });

});

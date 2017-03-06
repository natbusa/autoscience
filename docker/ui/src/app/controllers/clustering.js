/**
 * @ngdoc function
 * @name autoscienceApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the autoscienceApp
 */

app.controller('clusteringCtrl', function ($scope, $routeParams, $http) {
  var id= $routeParams.id;
  var vid= $routeParams.vid;
  $http({
    method: 'GET',
    url: '/cog/datasets/'+id+'/clustering/data'
  }).then(function successCallback(response) {
    // this callback will be called asynchronously
    // when the response is available
    $scope.c = response.data;
    console.log(response.data);
    $(".alert").alert('close');
  }, function errorCallback(response) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });

  $http({
    method: 'GET',
    url: '/cog/datasets/'+id+'/stats'
  }).then(function successCallback(response) {
    // this callback will be called asynchronously
    // when the response is available
    $scope.d = response.data;
    console.log(response.data);
  }, function errorCallback(response) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });

  $scope.chart=[];
  $http.get('/cog/datasets/'+id+'/clustering/charts/1').then(
    function (response) {    $scope.chart[1] = response.data; }
  );
  $http.get('/cog/datasets/'+id+'/clustering/charts/2').then(
    function (response) {    $scope.chart[2] = response.data; }
  );

});

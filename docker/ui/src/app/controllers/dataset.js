/**
 * @ngdoc function
 * @name autoscienceApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the autoscienceApp
 */
app.controller('datasetCtrl', function ($scope, $routeParams, $http) {
  var id= $routeParams.id;
  $http({
    method: 'GET',
    url: '/cog/datasets/'+id+'/stats'
  }).then(function successCallback(response) {
    // this callback will be called asynchronously
    // when the response is available
    $scope.d = response.data;

    $scope.chartsimg=[];
    $scope.chartdata=[];

    response.data.vars.forEach(function(item) {
      $http.get('/cog/datasets/'+id+'/variables/'+item.id+'/charts/1').then(
              function (response) { $scope.chartimg[item.id] = response.data; }
      );
      $http.get('/cog/datasets/'+id+'/variables/'+item.id).then(
              function (response) { $scope.chartdata[item.id] = response.data.var.stats.histogram; }
      );
    });

  }, function errorCallback(response) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });

  $scope.chartcolumns = [{"id": "c", "type": "bar", "name": "count"}];
  $scope.chartx = {"id": "v"};

});

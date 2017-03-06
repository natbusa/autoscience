/**
 * @ngdoc function
 * @name autoscienceApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the autoscienceApp
 */

app.controller('variableCtrl', function ($scope, $routeParams, $http) {
  var id= $routeParams.id;
  var vid= $routeParams.vid;
    $scope.chartc3 = {
      size: {
        height: 300
      },
      padding: {
        right: 30
      },
      data : {
        x: 'x',
        type: 'bar',
        rows: []
      },
      axis : {
        x : {
          type: 'category'
        }
      },
      tooltip: {
        format: {
          value: function (value, ratio, id) {
              return value;
          }
        }
      },
      legend: {
        show: false
      }
    };
  $scope.boxplot = false;
  $http({
    method: 'GET',
    url: '/cog/datasets/'+id+'/variables/'+vid
  }).then(function successCallback(response) {
    // this callback will be called asynchronously
    // when the response is available
    $scope.d = response.data;
    var vtype  = response.data.var.type.vtype;
    $scope.boxplot = vtype=='continuous' || vtype=='ordinal' || vtype=='descrete';

    var chartdata = response.data.var.stats.histogram.map(function(i) { return [i.v,i.c]; });
    chartdata = [['x', 'c']].concat(chartdata);
    $scope.chartc3.data.rows = chartdata;

    //logging
    console.log(chartdata);
  }, function errorCallback(response) {
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });

  $scope.chart = [];
  $http.get('/cog/datasets/'+id+'/variables/'+vid+'/charts/1').then(
    function (response) {    $scope.chart[1] = response.data; }
  );
  $http.get('/cog/datasets/'+id+'/variables/'+vid+'/charts/2').then(
    function (response) {    $scope.chart[2] = response.data; }
  );

});

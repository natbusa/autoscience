/**
 * @ngdoc overview
 * @name autoscienceApp
 * @description
 * # autoscienceApp
 *
 * Main module of the application.
 */

// Declare app level module which depends on filters, and services
var app= angular.module('autoscienceApp', [
  'ngRoute',
  'ngResource'
//  ,
//  'datatables',
//  'angular-c3-simple'
]);

app.config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'views/main.html'
    })
    .when('/about', {
      templateUrl: 'views/about.html',
      controller: 'aboutCtrl',
      controllerAs: 'about'
    })
    .when('/ds/:id/overview', {
      templateUrl: 'views/ds/overview.html',
      controller: 'datasetCtrl',
      controllerAs: 'dataset'
    })
    .when('/ds/:id/clustering', {
            templateUrl: 'views/ds/clustering.html',
            controller: 'clusteringCtrl',
            controllerAs: 'clustering'
    })
    .when('/ds/:id/variables/:vid', {
      templateUrl: 'views/ds/variables/overview.html',
      controller: 'variableCtrl',
      controllerAs: 'variable'
    })
    .otherwise({
      redirectTo: '/'
    });
});

app.config(['$locationProvider', function($locationProvider) {
  // use the HTML5 History API
  $locationProvider.html5Mode(true);
}]);

app.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrf';
  $httpProvider.defaults.xsrfHeaderName = 'X-csrf-token';
}]);

app.config(function ($httpProvider) {
  $httpProvider.interceptors.push([
    '$injector',
    function ($injector) {
      return $injector.get('AuthInterceptor');
    }
  ]);
});

app.factory('AuthInterceptor', function ($rootScope, $q, AUTH_EVENTS) {
  return {
    responseError: function (response) {
      $rootScope.$broadcast({
        401: AUTH_EVENTS.notAuthenticated,
        403: AUTH_EVENTS.notAuthorized,
        419: AUTH_EVENTS.sessionTimeout,
        440: AUTH_EVENTS.sessionTimeout
      }[response.status], response);
      return $q.reject(response);
    }
  };
});

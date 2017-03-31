app.config(function ($routeProvider) {
  $routeProvider
    .when('/datasets', {
      templateUrl: 'app/components/dataset/views/list.html',
      controller: 'DatasetListController'
    })
    .when('/new/dataset', {
      templateUrl: 'app/components/dataset/views/create.html',
      controller: 'DatasetCreateController'
    })
    .when('/datasets/:id', {
      templateUrl: 'app/components/dataset/views/sources.html',
      controller: 'DatasetController'
    })
    .when('/datasets/:id/settings', {
      templateUrl: 'app/components/dataset/views/settings.html',
      controller: 'DatasetSettingsController'
    });
});

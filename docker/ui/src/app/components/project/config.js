app.config(function ($routeProvider) {
  $routeProvider
    .when('/projects', {
      templateUrl: 'app/components/project/views/list.html',
      controller: 'ProjectListController'
    })
    .when('/new/project', {
      templateUrl: 'app/components/project/views/create.html',
      controller: 'ProjectCreateController'
    })
    .when('/projects/:pid', {
      templateUrl: 'app/components/project/views/show.html',
      controller: 'ProjectController'
    })
    .when('/projects/:pid/source', {
      templateUrl: 'app/components/project/views/source.html',
      controller: 'SourceController'
    })
    .when('/projects/:pid/source/setup', {
      templateUrl: 'app/components/project/views/source_setup.html',
      controller: 'SourceSetupController'
    })
    .when('/projects/:pid/edit', {
      templateUrl: 'app/components/project/views/edit.html',
      controller: 'ProjectController'
    })
    .when('/projects/:pid/settings', {
      templateUrl: 'app/components/project/views/settings.html',
      controller: 'ProjectController'
    });
});

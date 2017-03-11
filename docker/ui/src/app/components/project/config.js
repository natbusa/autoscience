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
    .when('/projects/:id', {
      templateUrl: 'app/components/project/views/show.html',
      controller: 'ProjectController'
    })
    .when('/projects/:id/edit', {
      templateUrl: 'app/components/project/views/edit.html',
      controller: 'ProjectController'
    })
    .when('/projects/:id/settings', {
      templateUrl: 'app/components/project/views/settings.html',
      controller: 'ProjectController'
    });
});

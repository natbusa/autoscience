app.config(function ($routeProvider) {
  $routeProvider
    .when('/projects', {
      templateUrl: 'app/components/project/project.list.view.html',
      controller: 'ProjectListController'
    })
    .when('/projects/:id', {
      templateUrl: 'app/components/project/project.show.view.html',
      controller: 'ProjectShowController'
    })
    .when('/projects/:id/edit', {
      templateUrl: 'app/components/project/project.edit.view.html',
      controller: 'ProjectEditController'
    })
    .when('/projects/create', {
      templateUrl: 'app/components/project/project.create.view.html',
      controller: 'ProjectCreateController'
    });
});

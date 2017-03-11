app.config(function ($routeProvider) {
  $routeProvider
    .when('/ideas', {
      templateUrl: 'app/components/idea/views/list.html',
      controller: 'IdeaListController'
    })
    .when('/new/idea', {
      templateUrl: 'app/components/idea/views/create.html',
      controller: 'IdeaCreateController'
    })
    .when('/ideas/:id', {
      templateUrl: 'app/components/idea/views/show.html',
      controller: 'IdeaController'
    })
    .when('/ideas/:id/edit', {
      templateUrl: 'app/components/idea/views/edit.html',
      controller: 'IdeaController'
    });
});

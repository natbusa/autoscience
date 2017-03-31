app.config(function ($routeProvider) {
  $routeProvider
    .when('/upload', {
      templateUrl: 'app/components/upload/views/upload.html',
      controller: 'FileUploadCtrl'
    });
});

app.controller('ProjectListController',function($scope,$location,Project){
    $scope.d=Project.query();
    $scope.show = function(id){
       $location.path('/projects/'+id);
    };
});

app.controller('ProjectController',function($scope,$routeParams,$location,Project){

    $scope.pid = $routeParams.pid;

    $scope.d=Project.get(
      {id:$routeParams.pid},
      function(){},
      function(){
        $location.path('/projects');
      }
    );

    $scope.delete=function(){
      $scope.d.$delete({id:$routeParams.pid},function(){
          $location.path('/projects');
      });
    };

    $scope.update=function(){
      $scope.d.$update({id:$routeParams.pid}, function(){
          $location.path('/projects');
      });
    };
});

app.controller('ProjectCreateController',function($scope,$location,$routeParams,Project){

    $scope.d=new Project();
    $scope.d.data = {type:'projects'};

    $scope.create=function(){
        $scope.d.$save(function(){
            $location.path('/projects/'+$scope.d.data.id);
        });
    };
});

app.controller('SourceSetupController',function($scope,$location,$routeParams,Project){

    $scope.pid = $routeParams.pid;

    $scope.d=Project.get(
      {id:$routeParams.pid},
      function(){
        $scope.loading = false;
        $scope.setup   = true;
      }
    );

    $scope.start=function(){
      $scope.setup = false;
      $scope.select = true;
    };

    $scope.datasets=Project.query();
    $scope.select_dataset = function(option){

    };

    $scope.update=function(){
      $scope.d.$update({id:$routeParams.pid}, function(){
        $location.path('/projects'+$scope.d.data.id);
      });
    };
});

app.controller('SourceController',function($scope,$location,$routeParams,Project){

    $scope.pid = $routeParams.pid;

    $scope.d=Project.get(
      {id:$routeParams.pid},
      function(){
      }
    );

    $scope.start=function(){
      $scope.setup = false;
      $scope.select = true;
    };

    $scope.datasets=Project.query();
    $scope.select_dataset = function(option){

    };

    $scope.update=function(){
      $scope.d.$update({id:$routeParams.pid}, function(){
        $location.path('/projects'+$scope.d.data.id);
      });
    };
});

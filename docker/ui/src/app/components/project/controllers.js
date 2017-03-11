app.controller('ProjectListController',function($scope,$location,Project){
    $scope.d=Project.query();
    $scope.show = function(id){
       $location.path('/projects/'+id);
    };
});

app.controller('ProjectController',function($scope,$routeParams,$location,Project){

    $scope.d=Project.get(
      {id:$routeParams.id},
      function(){},
      function(){
        $location.path('/projects');
      }
    );

    $scope.delete=function(){
      $scope.d.$delete({id:$routeParams.id},function(){
          $location.path('/projects');
      });
    };

    $scope.update=function(){
      $scope.d.$update({id:$routeParams.id}, function(){
          $location.path('/projects');
      });
    };
});

app.controller('ProjectCreateController',function($scope,$location,$routeParams,Project){

    $scope.setup = true;
    $scope.upload_form = false;
    $scope.preset_form = false;


    $scope.d=new Project();
    $scope.d.data = {type:'projects'};

    $scope.create=function(){
        $scope.d.$save(function(){
            $location.path('/projects');
        });
    };

    $scope.datasets=Project.query();
    $scope.select = function(option){
       $scope.setup  =false
       $scope.upload_form = option;
       $scope.preset_form = ! option;
    };

});

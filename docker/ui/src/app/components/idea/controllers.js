app.controller('IdeaListController',function($scope,$location,Idea){
    $scope.d=Idea.query();
    $scope.show = function(id){
       $location.path('/ideas/'+id);
    };
});

app.controller('IdeaController',function($scope,$routeParams,$location,Idea){

    $scope.d=Idea.get(
      {id:$routeParams.id},
      function(){},
      function(){
        $location.path('/ideas');
      }
    );

    $scope.delete=function(){
      $scope.d.$delete({id:$routeParams.id},function(){
          $location.path('/ideas');
      });
    };

    $scope.update=function(){
      $scope.d.$update({id:$routeParams.id}, function(){
          $location.path('/ideas');
      });
    };
});

app.controller('IdeaCreateController',function($scope,$location,$routeParams,Idea){

    $scope.d=new Idea();
    $scope.d.data = {type:'ideas'};

    $scope.create=function(){
        $scope.d.$save(function(){
            $location.path('/ideas');
        });
    };
});

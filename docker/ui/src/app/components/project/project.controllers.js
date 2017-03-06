app.controller('ProjectListController',function($scope,popupService,$window,Project){

    $scope.projects=Project.query();

    $scope.deleteProject=function(project){
        if(popupService.showPopup('Really delete this?')){
            project.$delete(function(){
                $window.location.href='';
            });
        }
    };

});

app.controller('ProjectShowController',function($scope,$routeParams,Project){

    $scope.project=Project.get({id:$routeParams.id});

});

app.controller('ProjectCreateController',function($scope,$location,$routeParams,Project){

    $scope.project=new Project();

    $scope.addProject=function(){
        $scope.project.$save(function(){
            $location.path('/projects');
        });
    };
});

app.controller('ProjectEditController',function($scope,$location,$routeParams,Project){

    $scope.updateProject=function(){
        $scope.project.$update(function(){
            $location.path('/projects');
        });
    };

    $scope.loadProject=function(){
        $scope.project=Project.get({id:$stateParams.id});
    };

    $scope.loadProject();
});

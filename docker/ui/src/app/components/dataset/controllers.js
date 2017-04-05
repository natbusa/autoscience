app.controller('DatasetListController',function($scope,$location,Dataset){
    $scope.d=Dataset.query();
    $scope.show = function(id){
       $location.path('/datasets/'+id);
    };
});

app.controller('DatasetController',function($scope,$routeParams,$location,Dataset){

    $scope.d=Dataset.get(
      {id:$routeParams.id},
      function(){},
      function(){
        $location.path('/datasets');
      }
    );

    $scope.delete=function(){
      $scope.d.$delete({id:$routeParams.id},function(){
          $location.path('/datasets');
      });
    };

    $scope.update=function(){
      $scope.d.$update({id:$routeParams.id}, function(){
          $location.path('/datasets');
      });
    };
});

app.controller('DatasetCreateController',function($scope,$location,$routeParams,Dataset){

    $scope.d=new Dataset();
    $scope.d.data = {type:'datasets'};

    $scope.create=function(){
        $scope.d.$save(function(){
            $location.path('/datasets');
        });
    };
});

app.controller('DatasetSettingsController',function($scope,$location,$routeParams,Dataset){

    $scope.id = $routeParams.id;

    $scope.d=Dataset.get(
      {id:$routeParams.id},
      function(){
        $scope.loading = false;
        $scope.setup   = true;
      }
    );

    $scope.start=function(){
      $scope.setup = false;
      $scope.select = true;
    };

    $scope.datasets=Dataset.query();
    $scope.select_dataset = function(option){

    };

    $scope.update=function(){
      $scope.d.$update({id:$routeParams.id}, function(){
        $location.path('/datasets'+$scope.d.data.id);
      });
    };
});

app.controller('FileUploadCtrl',function($scope, $routeParams, Source){

    $scope.files = [];
    $scope.progress = 0;
    $scope.progressVisible = false;

    id = $routeParams.id;
    $scope.fd=Source.query({'id':id});

    $scope.setFiles = function(element) {
      var files = [];
      for (var i = 0; i < element.files.length; i++) {
          files.push(element.files[i]);
      }
      $scope.$apply(function () { $scope.files = files; });
    };

    $scope.uploadFile = function() {

        id = $routeParams.id;

        var fd = new FormData();
        for (var i in $scope.files) {
            fd.append("file", $scope.files[i]);
        }

        var xhr = new XMLHttpRequest();

        xhr.upload.onprogress = function(evt) {
            if (evt.lengthComputable) {
                quota = Math.round(evt.loaded * 100 / evt.total);
                $scope.$apply(function () {
                   $scope.progress = quota;
                   $scope.progressVisible = true;
                });
                console.log(quota);
            } else {
                $scope.progress = 'unable to compute';
            }
        };

        xhr.addEventListener("load", uploadComplete, false);
        xhr.addEventListener("error", uploadFailed, false);
        xhr.addEventListener("abort", uploadCanceled, false);

        xhr.open("POST", "/api/data/datasets/"+id+"/files");

        xhr.send(fd);
    };

    function uploadComplete(evt) {
        /* This event is raised when the server send back a response */
        alert(evt.target.responseText);
        id = $routeParams.id;
        $scope.$apply(function () {
            $scope.fd=Source.query({'id':id});
            $scope.progressVisible = false;
        });
    }

    function uploadFailed(evt) {
        alert("There was an error attempting to upload the file.");
    }

    function uploadCanceled(evt) {
        $scope.progressVisible = false;
        alert("The upload has been canceled by the user or the browser dropped the connection.");
    }
});

app.controller('FileUploadCtrl',function($scope){

    $scope.files = [];
    $scope.progress = 0;
    $scope.progressVisible = false;

    $scope.setFiles = function(element) {
      var files = [];
      for (var i = 0; i < element.files.length; i++) {
          files.push(element.files[i]);
      }
      $scope.$apply(function () { $scope.files = files; });
    };

    $scope.uploadFile = function() {
        var fd = new FormData();
        for (var i in $scope.files) {
            fd.append("file", $scope.files[i]);
        }

        $scope.progressVisible = true;

        var xhr = new XMLHttpRequest();

        xhr.upload.onprogress = function(evt) {
            if (evt.lengthComputable) {
                quota = Math.round(evt.loaded * 100 / evt.total);
                $scope.$apply(function () { $scope.progress = quota; });
                console.log(quota);
            } else {
              $scope.progress = 'unable to compute';
            }
        };

        xhr.addEventListener("load", uploadComplete, false);
        xhr.addEventListener("error", uploadFailed, false);
        xhr.addEventListener("abort", uploadCanceled, false);

        xhr.open("POST", "/api/data/datasets");

        xhr.send(fd);
    };

    function uploadComplete(evt) {
        /* This event is raised when the server send back a response */
        alert(evt.target.responseText);
    }

    function uploadFailed(evt) {
        alert("There was an error attempting to upload the file.");
    }

    function uploadCanceled(evt) {
        $scope.progressVisible = false;
        alert("The upload has been canceled by the user or the browser dropped the connection.");
    }
});

app.factory('Project',function($resource, RESOURCE_API){
    return $resource(RESOURCE_API.url + '/projects/:id',{id:'@id'},{
        update: {
            method: 'PUT'
        }
    });
});

app.service('popupService',function($window){
    this.showPopup=function(message){
        return $window.confirm(message);
    };
});

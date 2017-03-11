app.factory('Project',function($resource, RESOURCES_API){
    return $resource(RESOURCES_API.url + '/projects/:id',{id:'@id'},{
        update: {
            method: 'PUT'
        },
        query: {
            method: 'GET',
            isArray:false
        }
    });
});

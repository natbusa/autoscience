app.factory('Idea',function($resource, RESOURCES_API){
    return $resource(RESOURCES_API.url + '/ideas/:id',{id:'@id'},{
        update: {
            method: 'PUT'
        },
        query: {
            method: 'GET',
            isArray:false
        }
    });
});

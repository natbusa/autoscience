app.factory('Dataset',function($resource, RESOURCES_API){
    return $resource(RESOURCES_API.url + '/datasets/:id',{id:'@id'},{
        update: {
            method: 'PUT'
        },
        query: {
            method: 'GET',
            isArray:false
        }
    });
});

app.factory('Source',function($resource, DATA_API){
    return $resource(DATA_API.url + '/datasets/:id/files/:fid',{fid:'@id'},{
        update: {
            method: 'PUT'
        },
        query: {
            method: 'GET',
            isArray:false
        }
    });
});

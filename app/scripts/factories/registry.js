angularApp.factory('Registry',["$resource",function($resource){
    return $resource('/api/registry',{},{
        read:{
            method:"GET",
            isArray:false
        },
        add:{
            method:"POST",
            isArray:false
        }
    });
}]);
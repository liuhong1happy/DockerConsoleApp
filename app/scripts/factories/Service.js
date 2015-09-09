angularApp.factory('Services',["$resource",function($resource){
    return $resource('/api/services',{},{
        read:{
            method:"GET",
            isArray:false
        }
    });
}]);
angularApp.factory('Service',["$resource",function($resource){

    return $resource('/api/service',{
    },{
        "submit":{
            method:"POST",
            isArray:false
        }
    });
}]);

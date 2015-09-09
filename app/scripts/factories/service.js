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
angularApp.factory('ServiceBuild',["$resource",function($resource){
    return $resource('/api/service/build',null,{
        "build":{
            method:"post",
            isArray:false
        }
    });
}]);

angularApp.factory('ServiceInfo',["$resource",function($resource){
    return $resource('/api/service/info',null,{
        "info":{
            method:"post",
            isArray:false
        }
    });
}]);

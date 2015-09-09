angularApp.factory('ApplicationRun',["$resource",function($resource){
    return $resource('/api/application/run',null,{
        "run":{
            method:"post",
            isArray:false
        }
    });
}]);
angularApp.factory('ApplicationInfo',["$resource",function($resource){
    return $resource('/api/application/info',null,{
        "info":{
            method:"post",
            isArray:false
        }
    });
}]);

angularApp.factory('Applications',["$resource",function($resource){
    return $resource('/api/applications',{},{
        read:{
            method:"GET",
            isArray:false
        }
    });
}]);
angularApp.factory('ApplicationAccess',["$resource",function($resource){
    return $resource('/api/application/access',null,{
        "start":{
            method:"POST",
            isArray:false
        },
        "find":{
            method:"GET",
            isArray:false
        }
    });
}]);

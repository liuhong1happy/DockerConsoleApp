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

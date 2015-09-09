angularApp.factory('GitLabToken',["$resource",function($resource){
    return $resource('/api/gitlab/token',null,{
        "getToken":{
            method:"get",
            isArray:false
        }
    });
}]);
      
angularApp.factory('GitLabRefresh',["$resource",function($resource){
    return $resource('/api/gitlab/refresh',null,{
        "refresh":{
            method:"get",
            isArray:false
        }
    });
}]);

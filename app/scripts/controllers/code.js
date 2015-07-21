'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:CodeCtrl
 * @description
 * # CodeCtrl
 * Controller of the angularApp
 */
angularApp.controller('CodeCtrl', ["$scope","config","$window","GitLabToken", function ($scope,config,$window,GitLabToken) {
    var env = config.envirement;
    var token = config[env].gitlab.token;
    var client_id = config[env].gitlab.client_id;
    var redirect_uri = config[env].gitlab.redirect_uri;
    var encodeUri = $window.encodeURIComponent(redirect_uri);
    $scope.authLink = token+ "?client_id="+client_id+"&redirect_uri="+encodeUri+"&response_type=code";
    GitLabToken.getToken({},function(res){
        if(res && res.status=="success"){
            if(res.data && res.data.access_token){
                $scope.hasToken = true; 
                // 根据token获取代码库列表
            }else{
                $scope.hasToken = false; 
            }
        }else{
            alert("服务器异常");
        }
    },function(e,err){
        alert("服务器错误");
    });
}]);

angularApp.factory('GitLabToken',["$resource",function($resource){
    return $resource('/api/gitlab/token',{
    },{
        "getToken":{
            method:"GET",
            isArray:false
        }
    });
}]);
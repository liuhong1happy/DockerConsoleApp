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
    $scope.authLink = token+ "?client_id="+client_id+"&redirect_uri="+redirect_uri+"&response_type=code";
    GitLabToken.getToken({},function(res){
        if(res && res.status=="success"){
            if(res.data && res.data.access_token){
                $scope.hasToken = true; 
                var tokenData = res.data;
                var user_info = tokenData.user_info;
                var groups_info = tokenData.groups_info;
                // 根据token获取代码库列表
                var users = []
                users.push({ "name":user_info.name, "projects":user_info.projects,"active":true });
                for(var i in groups_info){
                    var group = groups_info[i];
                    users.push({"name":group.name,"projects":group.details.projects,"active":false});
                }
                 $scope.users = users; 
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
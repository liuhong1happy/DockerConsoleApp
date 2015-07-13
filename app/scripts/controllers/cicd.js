'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:CicdCtrl
 * @description
 * # CicdCtrl
 * Controller of the angularApp
 */
angularApp.controller('CicdCtrl', ["$scope","config","Services","Service","$window","$timeout", function ($scope,config,Services,Service,$window,$timeout) {
    $scope.page_index = 0;
    $scope.page_size = 20;
    $scope.services = [];
    $scope.showList  = ["list","form","info"]
    $scope.showScope = $scope.showList[0];
    $scope.service_name = "";
    $scope.git_path = "";
    
    $timeout(function () {
            Services.read({
                "page_index":$scope.page_index,
                "page_size":$scope.page_size
            },function(res){
                if(res.status=="success"){
                    $scope.services = res.data;
                    $scope.$apply();
                    alert('请求成功');
                }else{
                    alert('数据为空');
                }
            },function(e,err){
                alert('请求失败');
            });
        }, 10);
    
    $scope.submitForm = function(isValid) {
                if (!isValid) {
                    alert('验证失败');
                }else{
                    Service.submit(null,{
                        user_name:"admin",
                        service_name:$scope.service_name,
                        git_path:$scope.git_path
                    },function(res){
                        alert('请求成功');
                    },function(e,err){
                        alert('请求失败');
                    }
                );
            }
    };
}]);
    
angularApp.factory('Services',["$resource",function($resource){
    return $resource('/api/services',{},{
        read:{
            method:"GET",
            isArray:false
        }
    });
}]);

angularApp.factory('Service',["$resource",function($resource){
    return $resource('/api/service',{},{
        "submit":{
            method:"POST",
            isArray:false
        }
    });
}]);

'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:CicdCtrl
 * @description
 * # CicdCtrl
 * Controller of the angularApp
 */
angularApp.controller('CicdCtrl', ["$scope","config","Services","$window", function ($scope,config,Services,$window) {
    $scope.page_index = 0;
    $scope.page_size = 20;
    $scope.services = [];
    $scope.showList  = ["list","form","info"]
    $scope.showScope = $scope.showList[0];
    $scope.service_name = "";
    $scope.git_path = "";
    
    Services.get(null,JSON.stringify({
        "page_index":$scope.page_index,
        "page_size":$scope.page_size
    },function(res){
        if(res.status=="success"){
            $scope.services = res.data;
            $scope.$apply();
        }
    },function(e,err){
        
    }));
}]);
    
angularApp.factory('Services',["$resource",function($resource){
    return $resource('/api/services',null,{
        "get":{
            method:"GET",isArray:true
        }
    });
}]);
    

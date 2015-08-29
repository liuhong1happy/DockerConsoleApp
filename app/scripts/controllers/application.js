'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:AppCtrl
 * @description
 * # AboutCtrl
 * Controller of the angularApp
 */
angularApp.controller('AppCtrl', ["$scope","config","$window","$timeout","Applications","ApplicationAccess",
function ($scope,config,$window,$timeout,Applications,ApplicationAccess) {
    $scope.page_index = 0;
    $scope.page_size = 20;
    $scope.applications = [];
    $timeout(function () {
            Applications.read({
                "page_index":$scope.page_index,
                "page_size":$scope.page_size
            },function(res){
                if(res.status=="success"){
                    $scope.applications = res.data;
                }else{
                    alert('数据为空');
                }
            },function(e,err){
                alert('请求失败');
            });
    }, 100);
    
    $scope.container_access = function(access_type,_id,content){
      ApplicationAccess.start(null,$.param({"type":access_type,"id":_id,"content":content}),function(res){
              if(res.status=="success"){
                    alert("操作成功");
                    if(access_type=="delete"){
                        var deleteIndex = -1;
                        for(var i=0;i<$scope.applications.length;i++){
                            if($scope.applications[i]._id == _id){
                                deleteIndex = i;
                            }
                        }
                        if(deleteIndex!=-1)
                            $scope.applications.splice(deleteIndex,1);
                    }
                }else{
                    alert(res.msg);
                }
      },function(e,err){
        alert('请求失败');
      })
    }
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

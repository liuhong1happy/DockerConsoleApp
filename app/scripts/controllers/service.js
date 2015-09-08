'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:CicdCtrl
 * @description
 * # CicdCtrl
 * Controller of the angularApp
 */
angularApp.controller('ServiceCtrl', ["$scope","config","Services","Service","ServiceInfo","ApplicationRun","ApplicationInfo","$window","$interval","$timeout", 
function ($scope,config,Services,Service,ServiceInfo,ApplicationRun,ApplicationInfo,$window,$interval,$timeout) {
    $scope.page_index = 0;
    $scope.page_size = 20;
    $scope.services = [];
    $scope.showList  = ["list","service","project"]
    $scope.showScope = $scope.showList[0];
    $scope.application_name = "";
    $scope.project_url = "";
    $scope.project_name = "";
    $scope.intervalId = null;
    var getContainerInfo = function(){
        if($scope.service==null) $interval.cancel($scope.intervalId);
        
        var application_id = $scope.service["application_id"];    
        ApplicationInfo.info(null,$.param({
          "application_id":application_id
        }),function(res){
          var run_status = res.data.status;
          var run_info = res.data.logs;
          $scope.service["run_status"] = run_status;
          $scope.service["run_info"] = run_info;
          if(run_status=="success"){
            $interval.cancel($scope.intervalId);
          }
        },function(e,err){
          $interval.cancel($scope.intervalId);
          $scope.service["run_status"] = "抱歉，网络原因无法得知当前状态";
          $scope.service["run_info"] = "抱歉,网络原因无法更新日志";
        });
    }
    
    $scope.create_application = function(project_name,project_url,storage_path){
      // 传递信息给后端，转到项目详情页面
      ApplicationRun.run(null,$.param({
        "project_name":project_name,
        "project_url":project_url,
        "storage_path":storage_path
      })
        ,function(res){
          $scope.service = null;
          for(var i in $scope.services){
            var service = $scope.services[i];
            if(service.project_url==project_url){
              $scope.service = service;
              
              $scope.service["application_id"] = res.data["_id"];
              $scope.service["run_status"] = "查询过程中...";
              $scope.service["run_info"] = "查询过程中..."
              $scope.showScope = $scope.showList[1];
              
              $scope.intervalId = $interval(getContainerInfo,1000);
              break;
            }
        }
          if($scope.service==null){
            alert("很抱歉，没有帮您找到服务的详细信息")
          }
        }
        ,function(e,err){
        alert("服务器错误");
      })
    }
    $scope.showServices = function(){
        $scope.showScope = $scope.showList[0];;
        $scope.service = null;
        
    }
    $scope.getImageInfo = function(){
        var project_name = $scope.project["project_name"];
        var project_url = $scope.project["project_url"];
        var project_id = $scope.project["project_id"];        
        ServiceInfo.info(null,$.param({
          "project_name":project_name,
          "project_url":project_url,
          "project_id":project_id
        }),function(res){
            var build_status = res.data.status;
            var build_info = res.data.logs;
            $scope.project["build_status"] = build_status;
            $scope.project["build_info"] = build_info;
            $window.console.log(build_info);
        },function(e,err){
          $scope.project["build_status"] = "抱歉，网络原因无法得知当前状态";
          $scope.project["build_info"] = "抱歉,网络原因无法更新日志";
        });
    }
    $scope.application_logs = function(project_name){
        for(var i=0;i<$scope.services.length;i++){
            if($scope.services[i].project_name == project_name){
                  $scope.project = $scope.services[i];
                  $scope.showScope = $scope.showList[2];
                  $scope.getImageInfo();
            }
        }
    }
    
    
    $timeout(function () {
            Services.read({
                "page_index":$scope.page_index,
                "page_size":$scope.page_size
            },function(res){
                if(res.status=="success"){
                    $scope.services = res.data;
                    
                }else{
                    alert('数据为空');
                }
            },function(e,err){
                alert('请求失败');
            });
        }, 100);
    
    $scope.submitForm = function(isValid) {
                if (!isValid) {
                    alert('验证失败');
                }else{
                    Service.submit(null, $.param({
                        user_name:"admin",
                        service_name:$scope.service_name,
                        git_path:$scope.git_path
                    }),function(res){
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

    return $resource('/api/service',{
    },{
        "submit":{
            method:"POST",
            isArray:false
        }
    });
}]);
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
'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:CodeCtrl
 * @description
 * # CodeCtrl
 * Controller of the angularApp
 */
angularApp.controller('CodeCtrl', ["$scope","config","$window","GitLabToken","ImageBuild","ImageInfo","$timeout", 
  function ($scope,config,$window,GitLabToken,ImageBuild,ImageInfo,$timeout) {
    var env = config.envirement;
    var token = config[env].gitlab.token;
    var client_id = config[env].gitlab.client_id;
    var redirect_uri = config[env].gitlab.redirect_uri;
    $scope.authLink = token+ "?client_id="+client_id+"&redirect_uri="+redirect_uri+"&response_type=code";
    $scope.showScope = "user";
    $scope.showUser = function(user_id){
      for(var u in $scope.users){
          $scope.users[u].active = false;
          if($scope.users[u].id==user_id){
            $scope.users[u].active = true;
          }
      }
    }
    
    var getImageInfo = function(){
        if($scope.project==null) $timeout.cancel(getImageInfo);
        project_name = $scope.project["name"];
        project_url = $scope.project["web_url"];
        project_id = $scope.project["id"];
        ImageInfo.info({},{
          "project_name":project_name,
          "project_url":project_url,
          "project_id":project_id
        },function(res){
          var build_status = res.data.build_status;
          var build_info = res.data.build_info;
          $scope.project["build_status"] = build_status;
          $scope.project["build_info"] = build_info;
          if(build_status=="success"){
            $timeout.cancel(getImageInfo);
          }
        },function(e,err){
          $timeout.cancel(getImageInfo);
          $scope.project["build_status"] = "抱歉，网络原因无法得知当前状态";
          $scope.project["build_info"] = "抱歉,网络原因无法更新日志";
        });
    }
    
    $scope.showUser = function(){
      $scope.showScope = "user";
      $scope.project = null;
    }
    
    $scope.showProject = function(user_id,project_id,project_name,project_url){
        $scope.project = null;
        for(var i in $scope.users){
          var user = $scope.users[i];
          for(var j in user.projects){
            var project = user.projects[j];
            if(project.web_url==project_url){
              $scope.project = project;
              $scope.project["build_status"] = "查询过程中...";
              $scope.project["build_info"] = "查询过程中..."
              $scope.showScope = "project";
              $timeout(getImageInfo,1000);
              break;
            }
          }
          if(user.id==user_id){
            break;
          }
        }
        if($scope.project==null){
          alert("很抱歉，没有帮您找到项目的详细信息")
        }
    }
    
    $scope.buildProject = function(user_id,project_id,project_name,project_url){
      // 传递信息给后端，转到项目详情页面
      ImageBuild.build({},{
        "project_name":project_name,
        "project_url":project_url,
        "project_id":project_id
      },function(res){
        $scope.project = null;
        for(var i in $scope.users){
          var user = $scope.users[i];
          for(var j in user.projects){
            var project = user.projects[j];
            if(project.web_url==project_url){
              $scope.project = project;
              $scope.project["build_status"] = "查询过程中...";
              $scope.project["build_info"] = "查询过程中..."
              $scope.showScope = "project";
              $timeout(getImageInfo,1000);
              break;
            }
          }
          if(user.id==user_id){
            break;
          }
        }
        if($scope.project==null){
          alert("很抱歉，没有帮您找到项目的详细信息")
        }
      },function(e,err){
        alert("服务器错误");
      })
    }
    
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

angularApp.factory('ServiceBuild',["$resource",function($resource){
    return $resource('/api/service/build',{
    },{
        "build":{
            method:"POST",
            isArray:false
        }
    });
}]);

angularApp.factory('ServiceInfo',["$resource",function($resource){
    return $resource('/api/service/info',{
    },{
        "info":{
            method:"POST",
            isArray:false
        }
    });
}]);

'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:CodeCtrl
 * @description
 * # CodeCtrl
 * Controller of the angularApp
 */
angularApp.controller('CodeCtrl', ["$scope","config","Util","$window","GitLabToken","GitLabRefresh","ServiceBuild","ServiceInfo","$interval", 
  function ($scope,config,Util,$window,GitLabToken,GitLabRefresh,ServiceBuild,ServiceInfo,$interval) {
      
     var getTokenByApi = function(){
        $window.console.log("get-token");
        GitLabToken.getToken({},function(res){
            if(res && res.status=="success"){
                if(res.data && res.data.access_token){
                    $scope.hasToken = true; 
                    var tokenData = res.data;
                    var user_info = tokenData.user_info;
                    var groups_info = tokenData.groups_info;
                    // 根据token获取代码库列表
                    var users = []
                    users.push({"id":"u"+user_info.id, "name":user_info.name, "projects":user_info.projects,"active":true });
                    for(var i in groups_info){
                        var group = groups_info[i];
                        users.push({"id":"g"+group.id,"name":group.name,"projects":group.details.projects,"active":false});
                    }
                    $scope.users = users; 
                    $window.console.log(users);
                    $scope.showScope = "user";

                }else{
                    $scope.hasToken = false; 
                    $scope.showLink();
                }
            }else{
                $scope.hasToken = false; 
                $scope.showLink();
            }
        },function(e,err){
            alert("服务器错误");
        });
     }

    $scope.showLink = function(){
            var env = config.envirement;
            var token = config[env].gitlab.token;
            var client_id = config[env].gitlab.client_id;
            var redirect_uri = config[env].gitlab.redirect_uri;
            $scope.auth_link = token+ "?client_id="+client_id+"&redirect_uri="+redirect_uri+"&response_type=code";
    }
    
    $scope.updateProjects = function(){
        GitLabRefresh.refresh({},function(res){
            getTokenByApi();
            alert("刷新成功");
        },function(e,err){
            alert("刷新错误");
        });
    }
      
    $scope.showScope = "user";
    $scope.activeUser = function(user_id){
        for(var u in $scope.users){
              $scope.users[u].active = false;
              if($scope.users[u].id==user_id){
                $scope.users[u].active = true;
              }
        }
        $scope.showScope = "user";
    }
    
    $scope.intervalId = null;
    $scope.getImageInfo = function(){
        if($scope.intervalId==null||$scope.project==null){
            return;
        }
        
        var project_name = $scope.project["name"];
        var project_url = $scope.project["web_url"];
        var project_id = $scope.project["id"];        
        ServiceInfo.info(null,$.param({
           "project_name":project_name,
           "project_url":project_url,
           "project_id":project_id
        }),function(res){
            
            var build_status = res.data.status;
            var build_info = res.data.logs;
            for(var i=0;i<build_info.length;i++){
                 build_info[i].log = Util.FormatLog(build_info[i].info);
            }
            $scope.project["build_status"] = build_status;
            $scope.project["build_info"] = build_info;
            if(build_status=="success"){
                $interval.cancel($scope.intervalId);
                $scope.intervalId = null;
            }
        },function(e,err){
          $interval.cancel($scope.intervalId);
          $scope.intervalId = null;
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
              $scope.intervalId = $interval($scope.getImageInfo,1000);
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
      ServiceBuild.build(null,$.param({
        "project_name":project_name,
        "project_url":project_url,
        "project_id":project_id
      }),function(res){
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
              $scope.intervalId =  $interval($scope.getImageInfo,1000);
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
      },
      function(e,err){
        alert("服务器错误");
      })
    }
    
    // 获取gitlab项目信息
    getTokenByApi();
}]);

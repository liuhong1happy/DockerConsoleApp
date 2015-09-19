'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:AppCtrl
 * @description
 * # AboutCtrl
 * Controller of the angularApp
 */
angularApp.controller('AppCtrl', ["$scope","config","$window","$timeout","Applications","ApplicationAccess","ApplicationInfo","Util","$interval",
function ($scope,config,$window,$timeout,Applications,ApplicationAccess,ApplicationInfo,Util,$interval) {
    $scope.page_index = 0;
    $scope.page_size = 20;
    $scope.applications = [];
    $scope.exec_logs = [];
    $scope.showList  = ["list","logs","application","exec"]
    $scope.showScope = $scope.showList[0];
    $timeout(function () {
            Applications.read({
                "page_index":$scope.page_index,
                "page_size":$scope.page_size
            },function(res){
                if(res.status=="success"){
                    var applications =  res.data;
                    for(var i=0;i<applications.length;i++){
                        var application = applications[i];
                        var ports = (application.inspect_container && application.inspect_container.NetworkSettings  && application.inspect_container.NetworkSettings.Ports)?application.inspect_container.NetworkSettings.Ports:[];
                        var tPorts = [];
                        for(var p in ports){
                            if(ports[p] && ports[p].length>0){
                                var tPort =  ports[p][0];
                                tPort["PortAndType"] = p;
                                tPorts.push(tPort)
                            }
                        }
                        $window.console.log(tPorts);
                        var urls = [];
                        for(var j=0;j<tPorts.length;j++){
                            var url = "http://"+(application.singleton?"":application.user_name+"-"+application.project_name+".")+application.address_prefix+":"+tPorts[j].HostPort;
                            urls.push({
                                "PortAndType":tPorts[j].PortAndType,
                                "PortUrl":url
                            });
                        }
                        $window.console.log(urls);
                        applications[i]["urls"] = urls;
                    }
                    $scope.applications = applications;
                }else{
                    alert('数据为空');
                }
            },function(e,err){
                alert('请求失败');
            });
    }, 100);
    $scope.showAppliactions = function(){
        $scope.showScope = $scope.showList[0];
    }
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
    
    $scope.getContainerInfo = function(_id){
        ApplicationInfo.info(null,$.param({
          "application_id":_id
        }),function(res){
            var run_status = res.data.status;
            var run_info = res.data.logs;
            for(var i=0;i<run_info.length;i++){
                 run_info[i].log = Util.FormatLog(run_info[i].info);
            }
            $scope.application["run_status"] = run_status;
            $scope.application["run_info"] = run_info;
        },function(e,err){
            $scope.application["run_status"] = "抱歉，网络原因无法得知当前状态";
            $scope.application["run_info"] = "抱歉,网络原因无法更新日志";
        });
    }
    // 获取构建日志
    $scope.show_run_logs = function(_id){
        // 获取日志
        for(var i=0;i<$scope.applications.length;i++){
            if($scope.applications[i]._id == _id){
                  $scope.application = $scope.applications[i];
                  $scope.showScope = $scope.showList[2];
                  $scope.getContainerInfo(_id);
            }
        }
    }
    
    $scope.getContainerLogs = function(){
        if($scope.container==null || $scope.container.status=="success") {
            $interval.cancel($scope.intervalId);
            return;
        }
        ApplicationAccess.find({
          "access_id":$scope.access_id
        },function(res){
            var status = res.data.status;
            var logs = res.data.logs;
            for(var i=0;i<logs.length;i++){
                 logs[i].log = Util.FormatLog(logs[i].info);
            }
            $scope.container["status"] = status;
            $scope.container["logs"] = logs;
            if(status=="success"){
               $interval.cancel($scope.intervalId);
            }
        },function(e,err){
            $interval.cancel($scope.intervalId);
            $scope.container["status"] = "抱歉，网络原因无法得知当前状态";
            $scope.container["logs"] = "抱歉,网络原因无法更新日志";
        });
    }
    
    // 获取容器日志
    $scope.show_container_logs = function(_id){
       $scope.container = {
            app_name:"",
            address:"",
            status:"start",
            logs:[]
       };
       // 获取日志
      for(var i=0;i<$scope.applications.length;i++){
            if($scope.applications[i]._id == _id){
                  var application = $scope.applications[i];
                  $scope.container["app_name"] =application["project_name"];
                  $scope.container["address"] =application["project_url"];
            }
        }
      ApplicationAccess.start(null,$.param({
          "type":"logs",
          "id":_id,
          "content":""
      }),function(res){
              if(res.status=="success"){
                     // 获取日志
                    $scope.access_id = res.data._id;
                    if($scope.intervalId) $interval.cancel($scope.intervalId);
                    $scope.intervalId = $interval($scope.getContainerLogs,3000);
                }else{
                    alert(res.msg);
                }
      },function(e,err){
        alert('请求失败');
      });
      // 切换视图
      $scope.showScope = $scope.showList[1];
    }
    
    // 追加交互日志
    $scope.append_exec_logs = function(){
        if($scope.exec==null || $scope.exec.status=="success") {
            $interval.cancel($scope.intervalId);
            return;
        }
        ApplicationAccess.find({
          "access_id":$scope.access_id
        },function(res){
            var status = res.data.status;
            var logs = res.data.logs;
            logs = logs.replace(/\n/gm,"<br/>");
            $scope.exec["status"] = status;
            $scope.exec.logs = $scope.exec.logs.concat([logs]);
            if(status=="success"){
                $interval.cancel($scope.intervalId);
                $scope.$input.focus();
                  $timeout(function(){
                      $scope.$exec.scrollTop($scope.$exec.find("ul").height());
                  },100);
            }
        },function(e,err){
            $interval.cancel($scope.intervalId);
            $scope.container["status"] = "抱歉，网络原因无法得知当前状态";
            $scope.container["logs"] = "抱歉,网络原因无法更新日志";
        });
    }
    $scope.show_exec = function(_id){
      // 查找application
      var findArr = $scope.applications.filter(function(item,index){
        return item._id==_id;
      });
       $scope.$input = angular.element(".console-input");
       $scope.$exec = angular.element(".exec-logs");
       $scope.$input.focus();
      if(findArr.length>=1){
          $scope.application = findArr[0];
          // 清空交互日志
          $scope.exec = {
            status: "success",
            logs: []
          }
          // 切换视图
          $scope.showScope = $scope.showList[3];
      }else{
          $window.console.log("没有找到容器");
      }
    }
    $scope.inputExecCMD = function(e){
        e = e || event;
        var currKey = e.keyCode||e.which||e.charCode;
        // 键入回车
        if(currKey==13){
            var value = $scope.exec.input_value;
            if(value=="clear"){
                $scope.exec = { status: "success", logs: [] };
                return;
            }
            if(value==""){
              $scope.exec.logs.push("");
              return;
            }
            $scope.exec.status = "start";
            $scope.exec.logs.push(value);
            $scope.$input.val("");
            ApplicationAccess.start(null,$.param({
                "type":"exec",
                "id":$scope.application._id,
                "content":value
            }),function(res){
                    if(res.status=="success"){
                           // 获取日志
                          $scope.access_id = res.data._id;
                          $timeout(function(){
                              $scope.$exec.scrollTop($scope.$exec.find("ul").height());
                          },100);
                          if($scope.intervalId) $interval.cancel($scope.intervalId);
                          $scope.intervalId = $interval($scope.append_exec_logs,3000);
                      }else{
                          alert(res.msg);
                      }
            },function(e,err){
              alert('请求失败');
            });
        }
    }
}]);

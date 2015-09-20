'use strict';
/**
 * @ngdoc function
 * @name angularApp.controller:RegistryCtrl
 * @description
 * # RegistryCtrl
 * Controller of the angularApp
 */
angularApp.controller('RegistryCtrl', ["$scope","config","$window","$timeout","Registry",  "$interval",
function ($scope,config,$window,$timeout,Registry,$interval) {
    $scope.showScope= "";
    $scope.registry = {
        status:"nostart",
        address:""
    };
    $timeout(function(){
        Registry.read(null,function(res){
            if(res.status=="success" && res.data){
                $scope.registry = res.data;
                if(res.data.inspect_container)
                    $scope.registry.address = res.data.run_host +":"+ res.data.inspect_container.NetworkSettings.Ports["5000/tcp"][0].HostPort;
            }else{
                $scope.registry = {
                    status:"nostart",
                    address:""
                };
            }
            $scope.showScope= "Inited";
        },function(e,err){
            $scope.showScope= "Inited";
        });
    },100);
    $scope.findRegistry = function(){
        if($scope.registry.status=="success"){
            $interval.cancel($scope.intervalId);
            return;
        }
        Registry.read(null,function(res){
            if(res.status=="success" && res.data){
                $scope.registry = res.data;
                if(res.data.inspect_container)
                    $scope.registry.address = res.data.run_host +":"+ res.data.inspect_container.NetworkSettings.Ports["5000/tcp"][0].HostPort;
            }else{
                $scope.registry = {
                    status:"nostart",
                    address:""
                };
            }
            $scope.showScope= "Inited";
        },function(e,err){
            $scope.showScope= "Inited";
        });
    };
    $scope.startRegistry = function(){
        Registry.add(null,$.param({}),function(res){
            if(res.status=="success"){
                $scope.registry = res.data;
                if($scope.registry.status!="success"){
                    $scope.intervalId = $interval($scope.findRegistry,3000);
                }
            }
            $scope.showScope= "Inited"
        },function(e,err){
            $scope.showScope= "Inited"
        });
    };          
}]);


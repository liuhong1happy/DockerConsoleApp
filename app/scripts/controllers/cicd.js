'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:CicdCtrl
 * @description
 * # CicdCtrl
 * Controller of the angularApp
 */
angularApp.controller('CicdCtrl', ["$scope","config", function ($scope,config) {
    var env = config.envirement;
    $scope.gitlabci = config[env].hrefs.test;   
    
    var resizeFunc = function(){
            var width = $($window).width();
            var height = $($window).height();
            $scope.gitlabci_width = width;
            $scope.gitlabci_height  = height-140;
            $scope.$apply();
    }
    
    $timeout(function(){
        resizeFunc();
    },10);
     
    $window.onresize =resizeFunc;
}]);

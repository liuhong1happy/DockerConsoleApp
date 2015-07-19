'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:CodeCtrl
 * @description
 * # CodeCtrl
 * Controller of the angularApp
 */
angularApp.controller('CodeCtrl', ["$scope","config","$timeout","$window", function ($scope,config,$timeout,$window) {
    var env = config.envirement;
    $scope.gitlab = config[env].hrefs.code;   
    
    var resizeFunc = function(){
            var width = $($window).width();
            var height = $($window).height();
            $scope.gitlab_width = width;
            $scope.gitlab_height  = height-140;
            $scope.$apply();
    }
    
    $timeout(function(){
        resizeFunc();
    },10);
     
    $window.onresize =resizeFunc;
}]);

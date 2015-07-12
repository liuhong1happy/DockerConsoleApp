'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the angularApp
 */
angularApp.controller('BookCtrl', ["$scope","config","$window","$timeout",  function ($scope,config,$window,$timeout) {
    var env = config.envirement;
    $scope.gitbook = config[env].hrefs.book;   
    
    var resizeFunc = function(){
            var width = $($window).width();
            var height = $($window).height();
            $scope.gitbook_width = width;
            $scope.gitbook_height  = height-140;
            $scope.$apply();
    }
    
    $timeout(function(){
        resizeFunc();
    },10);
     
    $window.onresize =resizeFunc;
}]);


angularApp.controller("navHeader",["$scope","config","$location",function($scope,config,$location){
    var url = $location.url();
    var env = config.envirement;
    $scope.book = config[env].hrefs.book;
    $scope.activeNav = url;
}]);

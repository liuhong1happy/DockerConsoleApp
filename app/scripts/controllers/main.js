'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the angularApp
 */
angularApp.factory("carouselService", function(){
    var carousel = {
        classes:["jumb_1","jumb_2","jumb_3","jumb_4","jumb_5","jumb_6","jumb_7"],
        current_index:0
    }
    return carousel;
});

angularApp.controller('MainCtrl', ["$scope","$window","$document","$rootScope","carouselService", function ($scope,$window,$document,$rootScope,carouselService,navService) {
        $scope.classes = carouselService.classes;
        $scope.index = carouselService.current_index;
        $scope.$watch("index",function(newValue, oldValue){
            var _class = $scope.classes[$scope.index];
            var parentElement = $("."+_class);
            var top = $scope.index==0?0: parentElement.position().top;
            parentElement.find("h1").css({position:"relative",left:-450,top:0}).animate({left:0 },"slow");
            parentElement.find(".descript").css({position:"relative",left:450,top:0}).animate({left:0 },"slow");
            parentElement.find(".link").css({position:"relative",left:-450,top:0}).animate({left:0 },"slow");
            
            $($window.document.body).animate({ scrollTop: top }, 'slow');
        });
      
       var toTop = function(){
            if($scope.index <= 0){
                $scope.index = 0;
            }else{
                $scope.index -= 1;
            }
       }
       
       var toBottom = function(){
            var length = $scope.classes.length;
            if($scope.index >= length-1){
                $scope.index = length-1;
            }else{
                $scope.index += 1;
            }
       }
      
        $window.onkeydown = function (e) {
                e = e || event;
                var target = e.target || e.srcElement;
                var keyCode = e.which ? e.which : e.keyCode;
                switch (keyCode) {
                    //pageUp
                    case 33:
                    //2键
                    case 104:
                    //W/w键
                    case 87:
                    case 119:
                    //上键
                    case 38:
                        toTop();
                        break;
                    //pageDown
                    case 34:
                    //8键
                    case 98:
                    //S/s键
                    case 83:
                    case 115:
                    //下键
                    case 40:
                        toBottom();
                        break;
                    //Home键
                    case 36:
                        $scope.index = 0;
                        break;
                    //End键
                    case 35:
                        $scope.index = $scope.classes.length -1;
                        break;
                    default:
                        break;  
                }
            e.stopPropagation ? e.stopPropagation() : e.cancelBubble = true;
            e.preventDefault ? e.preventDefault() : e.returnValue = false;
            $scope.$apply();
            return false;
        }
        $window.onmousewheel = function(e){
            var e = e || event;
            var wheelDelta = e.wheelDelta || -e.detail * 40;
            if (wheelDelta > 0) {
                           toTop();
            }else{
                           toBottom();
            }
            $scope.$apply();
        };
      
  }]);

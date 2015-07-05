'use strict';

/**
 * @ngdoc overview
 * @name angularApp
 * @description
 * # angularApp
 *
 * Main module of the application.
 */
var angularApp = angular
  .module('angularApp', [
    'ngAnimate',
    'ngAria',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch'
  ])

 angularApp.config(["$interpolateProvider", function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
  }]);

  angularApp.config(["$routeProvider", function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/book', {
        templateUrl: 'views/book.html',
        controller: 'BookCtrl',
        controllerAs: 'book'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about'
      })
      .otherwise({
        redirectTo: '/'
      });
  }]);

angularApp.factory("config",function(){
    var config = {
        envirement:"dev",
        dev:{
            hrefs:{
                book:"http://localhost:4000"
            }
        },
        pro:{
            hrefs:{
                book:"http://docs.dockerdocs.cn"
            }
        }
    }
    return config;
});

angularApp.config(["$sceDelegateProvider", function($sceDelegateProvider) {
  $sceDelegateProvider.resourceUrlWhitelist([
    // Allow same origin resource loads.
    'self',
    // Allow loading from our assets domain.  Notice the difference between * and **.
    'http://*.dockerdocs.cn/**',
    'http://*.docker.io/**',
    'http://*.docker.com/**',
    'http://localhost:4000/**'
  ]);
}]);

angularApp.controller("navHeader",["$scope","config","$location",function($scope,config,$location){
    var url = $location.url();
    var env = config.envirement;
    $scope.book = config[env].hrefs.book;
    $scope.activeNav = url;
    $scope.$apply();
}]);

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


'use strict';

/**
 * @ngdoc function
 * @name angularApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the angularApp
 */
angularApp
  .controller('AboutCtrl', ["$scope",function ($scope) {    

  }]);

angular.module('angularApp').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('views/about.html',
    "<p>This is the about view.</p>"
  );


  $templateCache.put('views/book.html',
    "<iframe src=\"[[gitbook]]\" frameborder=\"0\" width=\"[[gitbook_width]]\" height=\"[[gitbook_height]]\" style=\"margin:-20px -15px -5px -15px;padding:0px\" scrolling=\"no\"></iframe>"
  );


  $templateCache.put('views/main.html',
    "<div class=\"jumbotron firstJumbotron text-center jumb_1\"> <h1>社区文档阅读</h1> <p class=\"descript\"> <span class=\"glyphicon glyphicon-book book-icon\"></span><br> 《Docker官方文档中文翻译》 </p> <p class=\"link\"><a class=\"btn btn-lg btn-success\" ng-href=\"#/book\">阅&nbsp;&nbsp;&nbsp;&nbsp;读</a></p> </div> <div class=\"jumbotron whiteJumbotron text-center jumb_2\"> <h1>社区代码托管</h1> <p class=\"descript\"> <span class=\"glyphicon glyphicon-file book-icon\"></span><br> 借助Gitlab开源代码托管工具，对社区项目以及社区会员代码进行托管。 </p> <p class=\"link\"><a class=\"btn btn-lg btn-success\" ng-href=\"#/\">开始托管</a></p> </div> <div class=\"jumbotron blueJumbotron text-center jumb_3 animate-if\"> <h1>社区持续集成</h1> <p class=\"descript\"> <span class=\"glyphicon glyphicon-refresh book-icon\"></span><br> 借助Gitlab CI持续集成工具，以及社区自己开发的自动部署工具，快速构建镜像和启动应用服务。 </p> <p class=\"link\"><a class=\"btn btn-lg btn-success\" ng-href=\"#/\">快速集成</a></p> </div> <div class=\"jumbotron grayJumbotron text-center jumb_4 animate-if\"> <h1>社区镜像管理</h1> <p class=\"descript\"> <span class=\"glyphicon glyphicon-duplicate book-icon\"></span><br> 你可以管理自己构建的镜像，以及查看社区维持的镜像，你可以通过这些镜像快速启动你的应用服务。 </p> <p class=\"link\"><a class=\"btn btn-lg btn-success\" ng-href=\"#/\">镜像查看</a></p> </div> <div class=\"jumbotron whiteJumbotron text-center jumb_5 animate-if\"> <h1>社区应用管理</h1> <p class=\"descript\"> <span class=\"glyphicon glyphicon-console book-icon\"></span><br> 社区上通过镜像部署的应用，你可以放心的托管和管理。 </p> <p class=\"link\"><a class=\"btn btn-lg btn-success\" ng-href=\"#/\">我的应用</a></p> </div> <div class=\"jumbotron blueJumbotron text-center jumb_6 animate-if\"> <h1>社区加速器</h1> <p class=\"descript\"> <span class=\"glyphicon glyphicon-plane book-icon\"></span><br> 如果官方下载速度无法满足你下载的要求时，考虑社区加速器，让你的下载杠杠的。 </p> <p class=\"link\"><a class=\"btn btn-lg btn-success\" ng-href=\"#/\">我要加速</a></p> </div> <div class=\"jumbotron grayJumbotron text-center jumb_7 animate-if\"> <h1>参与社区建设</h1> <p class=\"descript\"> <span class=\"glyphicon glyphicon-map-marker book-icon\"></span><br> 社区目前处于建设阶段，需要广大的社区成员加入。<br> Let's go！让我们一起来创建更好的社区体验。 </p> <p class=\"link\"><a class=\"btn btn-lg btn-success\" ng-href=\"#/\">加入我们</a></p> </div>"
  );

}]);

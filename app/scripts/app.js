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
  ]);

 angularApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
  });

 angularApp.config(function($httpProvider) {
     $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
     $httpProvider.defaults.headers.put['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
     $httpProvider.defaults.headers.common["Accept"] = 'application/json, text/plain, * / *';
     $httpProvider.defaults.headers.common["x-Requested-With"] = "XMLHttpRequest";
      $httpProvider.defaults.transformRequest = [function(data) {
        return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
      }];
 });

  angularApp.config(function ($routeProvider) {
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
      .when('/code', {
        templateUrl: 'views/code.html',
        controller: 'CodeCtrl',
        controllerAs: 'code'
      })
      .when('/service', {
        templateUrl: 'views/service.html',
        controller: 'ServiceCtrl',
        controllerAs: 'service'
      })
      .when('/application', {
        templateUrl: 'views/application.html',
        controller: 'AppCtrl',
        controllerAs: 'application'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about'
      })
      .otherwise({
        redirectTo: '/'
      });
  });

angularApp.factory("config",function(){
    var config = {
        envirement:"dev",
        dev:{
            hrefs:{
                book:"http://www.dockerconsole.com:4000",
                code:"http://www.dockerconsole.com:10080",
                test:"http://www.dockerconsole.com:10081",
            },
            gitlab:{
                token:"http://www.dockerconsole.com:10080/oauth/authorize",
                client_id:"85f65cd2239dcb49996e1eff34d375db40c2d8af7af2cbac17a2826ca3c1ebfc",
                redirect_uri:"http://www.dockerconsole.com:8888/api/gitlab/oauth",
            }
        },
        pro:{
            hrefs:{
                book:"http://docs.dockerdocs.cn",
                code:"http://gitlab.dockerdocs.cn",
                test:"http://gitlabci.dockerdocs.cn",

            },
            gitlab:{
                token:"http://gitlab.dockerdocs.cn/oauth/authorize",
                client_id:"85f65cd2239dcb49996e1eff34d375db40c2d8af7af2cbac17a2826ca3c1ebfc",
                redirect_uri:"http://gitlab.dockerdocs.cn/api/gitlab/oauth",
            }
        }
    }
    return config;
});

angularApp.config(function($sceDelegateProvider) {
  $sceDelegateProvider.resourceUrlWhitelist([
    // Allow same origin resource loads.
    'self',
    // Allow loading from our assets domain.  Notice the difference between * and **.
    'http://*.dockerdocs.cn/**',
    'http://*.docker.io/**',
    'http://*.docker.com/**',
    'http://www.dockerconsole.com:4000/**',   // gitbook
    'http://www.dockerconsole.com:10080/**',  // gitlab
    'http://www.dockerconsole.com:10081/**',  // gitlab ci
  ]);
});

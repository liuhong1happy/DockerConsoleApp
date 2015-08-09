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
                book:"http://192.168.0.110:4000",
                code:"http://localhost:10080",
                test:"http://192.168.0.110:10081",
            },
            gitlab:{
                token:"http://192.168.0.110:10080/oauth/authorize",
                client_id:"01841bc629e150c25d3eddffc23edc4092f86aad0c1d58fef67305a125ee2b90",
                redirect_uri:"http://192.168.0.110:8888/api/gitlab/oauth",
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
                client_id:"01841bc629e150c25d3eddffc23edc4092f86aad0c1d58fef67305a125ee2b90",
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
    'http://localhost:4000/**',   // gitbook
    'http://localhost:10080/**',  // gitlab
    'http://localhost:10081/**',  // gitlab ci
  ]);
});

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

 angularApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
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

angularApp.config(function($sceDelegateProvider) {
  $sceDelegateProvider.resourceUrlWhitelist([
    // Allow same origin resource loads.
    'self',
    // Allow loading from our assets domain.  Notice the difference between * and **.
    'http://*.dockerdocs.cn/**',
    'http://*.docker.io/**',
    'http://*.docker.com/**',
    'http://localhost:4000/**'
  ]);
});

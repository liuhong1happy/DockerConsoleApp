"use strict";var angularApp=angular.module("angularApp",["ngAnimate","ngAria","ngCookies","ngMessages","ngResource","ngRoute","ngSanitize","ngTouch"]);angularApp.config(["$interpolateProvider",function(a){a.startSymbol("[["),a.endSymbol("]]")}]),angularApp.config(["$httpProvider",function(a){a.defaults.headers.post["Content-Type"]="application/x-www-form-urlencoded;charset=utf-8",a.defaults.headers.put["Content-Type"]="application/x-www-form-urlencoded;charset=utf-8",a.defaults.headers.common.Accept="application/json, text/plain, * / *",a.defaults.headers.common["x-Requested-With"]="XMLHttpRequest",a.defaults.transformRequest=[function(a){return angular.isObject(a)&&"[object File]"!==String(a)?param(a):a}]}]),angularApp.config(["$routeProvider",function(a){a.when("/",{templateUrl:"views/main.html",controller:"MainCtrl",controllerAs:"main"}).when("/book",{templateUrl:"views/book.html",controller:"BookCtrl",controllerAs:"book"}).when("/code",{templateUrl:"views/code.html",controller:"CodeCtrl",controllerAs:"code"}).when("/cicd",{templateUrl:"views/cicd.html",controller:"CicdCtrl",controllerAs:"cicd"}).when("/about",{templateUrl:"views/about.html",controller:"AboutCtrl",controllerAs:"about"}).otherwise({redirectTo:"/"})}]),angularApp.factory("config",function(){var a={envirement:"dev",dev:{hrefs:{book:"http://192.168.0.110:4000",code:"http://192.168.0.110:10080",test:"http://192.168.0.110:10081"},gitlab:{token:"http://192.168.0.110:10080/oauth/authorize",client_id:"9c7a33a2ed9dbe2ef77d91f9fd9c27de495ad8a68ae0609556401b09f7245d98",redirect_uri:"http://192.168.0.110:8888/api/gitlab/oauth"}},pro:{hrefs:{book:"http://docs.dockerdocs.cn",code:"http://gitlab.dockerdocs.cn",test:"http://gitlabci.dockerdocs.cn"},gitlab:{token:"http://gitlab.dockerdocs.cn/oauth/authorize",client_id:"9c7a33a2ed9dbe2ef77d91f9fd9c27de495ad8a68ae0609556401b09f7245d98",redirect_uri:"http://gitlab.dockerdocs.cn/api/gitlab/oauth"}}};return a}),angularApp.config(["$sceDelegateProvider",function(a){a.resourceUrlWhitelist(["self","http://*.dockerdocs.cn/**","http://*.docker.io/**","http://*.docker.com/**","http://localhost:4000/**","http://localhost:10080/**","http://localhost:10081/**"])}]),angularApp.controller("navHeader",["$scope","config","$location",function(a,b,c){var d=c.url(),e=b.envirement;a.book=b[e].hrefs.book,a.gitlab=b[e].hrefs.code,a.activeNav=d}]),angularApp.factory("carouselService",function(){var a={classes:["jumb_1","jumb_2","jumb_3","jumb_4","jumb_5","jumb_6","jumb_7"],current_index:0};return a}),angularApp.controller("MainCtrl",["$scope","$window","$document","$rootScope","carouselService",function(a,b,c,d,e,f){a.classes=e.classes,a.index=e.current_index,a.$watch("index",function(c,d){var e=a.classes[a.index],f=$("."+e),g=0==a.index?0:f.position().top;f.find("h1").css({position:"relative",left:-450,top:0}).animate({left:0},"slow"),f.find(".descript").css({position:"relative",left:450,top:0}).animate({left:0},"slow"),f.find(".link").css({position:"relative",left:-450,top:0}).animate({left:0},"slow"),$(b.document.body).animate({scrollTop:g},"slow")});var g=function(){a.index<=0?a.index=0:a.index-=1},h=function(){var b=a.classes.length;a.index>=b-1?a.index=b-1:a.index+=1};b.onkeydown=function(b){b=b||event;var c=(b.target||b.srcElement,b.which?b.which:b.keyCode);switch(c){case 33:case 104:case 87:case 119:case 38:g();break;case 34:case 98:case 83:case 115:case 40:h();break;case 36:a.index=0;break;case 35:a.index=a.classes.length-1}return b.stopPropagation?b.stopPropagation():b.cancelBubble=!0,b.preventDefault?b.preventDefault():b.returnValue=!1,a.$apply(),!1},b.onmousewheel=function(b){var b=b||event,c=b.wheelDelta||40*-b.detail;c>0?g():h(),a.$apply()}}]),angularApp.controller("BookCtrl",["$scope","config","$window","$timeout",function(a,b,c,d){var e=b.envirement;a.gitbook=b[e].hrefs.book;var f=function(){var b=$(c).width(),d=$(c).height();a.gitbook_width=b,a.gitbook_height=d-140,a.$apply()};d(function(){f()},10),c.onresize=f}]),angularApp.controller("CicdCtrl",["$scope","config","Services","Service","$window","$timeout",function(a,b,c,d,e,f){a.page_index=0,a.page_size=20,a.services=[],a.showList=["list","form","info"],a.showScope=a.showList[0],a.service_name="",a.git_path="",f(function(){c.read({page_index:a.page_index,page_size:a.page_size},function(b){"success"==b.status?a.services=b.data:alert("数据为空")},function(a,b){alert("请求失败")})},10),a.submitForm=function(b){b?d.submit(null,$.param({user_name:"admin",service_name:a.service_name,git_path:a.git_path}),function(a){alert("请求成功")},function(a,b){alert("请求失败")}):alert("验证失败")}}]),angularApp.factory("Services",["$resource",function(a){return a("/api/services",{},{read:{method:"GET",isArray:!1}})}]),angularApp.factory("Service",["$resource",function(a){return a("/api/service",{},{submit:{method:"POST",isArray:!1}})}]),angularApp.controller("CodeCtrl",["$scope","config","$window","GitLabToken","ServiceBuild","ServiceInfo","$timeout",function(a,b,c,d,e,f,g){var h=b.envirement,i=b[h].gitlab.token,j=b[h].gitlab.client_id,k=b[h].gitlab.redirect_uri;a.authLink=i+"?client_id="+j+"&redirect_uri="+k+"&response_type=code",a.showScope="user",a.activeUser=function(b){for(var c in a.users)a.users[c].active=!1,a.users[c].id==b&&(a.users[c].active=!0);a.showScope="user"};var l=function(){null==a.project&&g.cancel(l);var b=a.project.name,c=a.project.web_url,d=a.project.id;f.info(null,$.param({project_name:b,project_url:c,project_id:d}),function(b){var c=b.data.status,d=b.data.logs;a.project.build_status=c,a.project.build_info=d,"success"==c&&g.cancel(l)},function(b,c){g.cancel(l),a.project.build_status="抱歉，网络原因无法得知当前状态",a.project.build_info="抱歉,网络原因无法更新日志"})};a.showUser=function(){a.showScope="user",a.project=null},a.showProject=function(b,c,d,e){a.project=null;for(var f in a.users){var h=a.users[f];for(var i in h.projects){var j=h.projects[i];if(j.web_url==e){a.project=j,a.project.build_status="查询过程中...",a.project.build_info="查询过程中...",a.showScope="project",g(l,1e3);break}}if(h.id==b)break}null==a.project&&alert("很抱歉，没有帮您找到项目的详细信息")},a.buildProject=function(b,c,d,f){e.build(null,$.param({project_name:d,project_url:f,project_id:c}),function(c){a.project=null;for(var d in a.users){var e=a.users[d];for(var h in e.projects){var i=e.projects[h];if(i.web_url==f){a.project=i,a.project.build_status="查询过程中...",a.project.build_info="查询过程中...",a.showScope="project",g(l,1e3);break}}if(e.id==b)break}null==a.project&&alert("很抱歉，没有帮您找到项目的详细信息")},function(a,b){alert("服务器错误")})},d.getToken({},function(b){if(b&&"success"==b.status)if(b.data&&b.data.access_token){a.hasToken=!0;var d=b.data,e=d.user_info,f=d.groups_info,g=[];g.push({id:"u"+e.id,name:e.name,projects:e.projects,active:!0});for(var h in f){var i=f[h];g.push({id:"g"+i.id,name:i.name,projects:i.details.projects,active:!1})}a.users=g,c.console.log(g),a.showScope="user"}else a.hasToken=!1;else alert("服务器异常")},function(a,b){alert("服务器错误")})}]),angularApp.factory("GitLabToken",["$resource",function(a){return a("/api/gitlab/token",null,{getToken:{method:"get",isArray:!1}})}]),angularApp.factory("ServiceBuild",["$resource",function(a){return a("/api/service/build",null,{build:{method:"post",isArray:!1}})}]),angularApp.factory("ServiceInfo",["$resource",function(a){return a("/api/service/info",null,{info:{method:"post",isArray:!1}})}]),angularApp.controller("AboutCtrl",["$scope",function(a){}]),angular.module("angularApp").run(["$templateCache",function(a){a.put("views/about.html","<p>This is the about view.</p>"),a.put("views/book.html",'<iframe src="[[gitbook]]" frameborder="0" width="[[gitbook_width]]" height="[[gitbook_height]]" style="margin:-20px -15px -5px -15px;padding:0px" scrolling="no"></iframe>'),a.put("views/cicd.html",'<div class="row" style="margin:20px 120px"> <h2>代码构建</h2> <p>我们需要自动化去部署代码，必然会面临代码构建成容器镜像，本步骤即为构建镜像</p> <a class="btn btn-success" ng-click="showScope=\'form\'">创建任务</a> <hr> </div> <div class="row" ng-show="showScope==\'list\'" style="margin:20px 120px"> <table class="table"> <thead> <tr> <td>任务名称</td> <td>代码源</td> <td>构建状态</td> <td>镜像名称</td> <td>更新时间</td> </tr> </thead> <tbody> <tr ng-repeat="service in services"> <td>[[service.name]]</td> <td>[[service.code]]</td> <td>[[service.status]]</td> <td>[[service.image]]</td> <td>[[ (service.update_time?service.update_time:service.create_time)*1000 | date:"yyyy-MM-dd hh:mm:ss"]]</td> </tr> </tbody> </table> </div> <div class="row" ng-show="showScope==\'form\'" style="margin:20px 120px"> <form role="form" name="service_form" class="form-horizontal" ng-submit="submitForm(service_form.$valid)" novalidate> <div class="form-group has-feedback"> <label class="col-xs-2">任务名称</label> <div class="col-xs-10"> <input type="text" class="form-control" name="service_name" ng-model="service_name" required ng-maxlength="20"> <span class="glyphicon glyphicon-ok form-control-feedback" ng-show="service_form.service_name.$dirty && service_form.service_name.$valid"></span> </div> </div> <div class="form-group has-feedback"> <label class="col-xs-2">代码位置</label> <div class="col-xs-10"> <input type="text" class="form-control" name="git_path" ng-model="git_path" required ng-maxlength="200"> <span class="glyphicon glyphicon-ok form-control-feedback" ng-show="service_form.git_path.$dirty && service_form.git_path.$valid"></span> </div> </div> <div class="form-group has-feedback"> <input class="btn btn-success" type="submit" ng-disabled="service_form.$invalid" value="提交"> </div> </form> </div>'),a.put("views/code.html",'<div class="row" style="margin:20px 120px" ng-show="showScope==\'user\'"> <h2>代码托管</h2> <p>我们需要获取你gitlab代码库列表，以便实现镜像自动构建、持续集成和自动部署</p> <a ng-hide="hasToken" class="btn btn-success" ng-href="authLink">开启托管</a> <hr> </div> <div class="row" ng-show="hasToken && showScope==\'user\'" style="margin:20px 120px"> <div class="tab-nav"> <ul class="ul-nav nav nav-tabs"> <li role="presentation" ng-repeat="user in users" ng-class="user.active?\'active\':\'\';" ng-style="user.active?{}:{}"> <a ng-click="activeUser(user.id)"> [[user.name]]</a> </li> </ul> <ul class="nav nav-pills" ng-repeat="user in users" ng-show="user.active" style="border:1px solid #ddd;border-top:0px solid transparent;padding-top:10px"> <li role="presentation" ng-repeat="project in user.projects" style="margin:0px 20px 20px;padding:20px;border:1px solid #00a28d"> <div class="project-avatar">[[project.avatar_url]]</div> <div class="project-name">[[project.name]]</div> <div class="project-url">[[project.web_url]]</div> <div class="project-link"> <a ng-click="buildProject(user.id,project.id,project.name,project.web_url)">构建镜像</a> </div> </li> </ul> </div> </div> <div class="row" ng-show="showScope==\'project\'"> <h2>[[project.name]]</h2> <p>[[project.web_url]]</p> <p>[[project.build_status]]</p> <a ng-click="showUser()">返回</a> <hr> </div> <div class="row" ng-show="showScope==\'project\'"> <div class="build-info"> [[project.build_info]] </div> </div>'),a.put("views/main.html",'<div class="jumbotron firstJumbotron text-center jumb_1"> <h1>社区文档阅读</h1> <p class="descript"> <span class="glyphicon glyphicon-book book-icon"></span><br> 《Docker官方文档中文翻译》 </p> <p class="link"><a class="btn btn-lg btn-success" ng-href="#/book">阅&nbsp;&nbsp;&nbsp;&nbsp;读</a></p> </div> <div class="jumbotron whiteJumbotron text-center jumb_2"> <h1>社区代码托管</h1> <p class="descript"> <span class="glyphicon glyphicon-file book-icon"></span><br> 借助Gitlab开源代码托管工具，对社区项目以及社区会员代码进行托管。 </p> <p class="link"><a class="btn btn-lg btn-success" ng-href="#/">开始托管</a></p> </div> <div class="jumbotron blueJumbotron text-center jumb_3 animate-if"> <h1>社区持续集成</h1> <p class="descript"> <span class="glyphicon glyphicon-refresh book-icon"></span><br> 借助Gitlab CI持续集成工具，以及社区自己开发的自动部署工具，快速构建镜像和启动应用服务。 </p> <p class="link"><a class="btn btn-lg btn-success" ng-href="#/">快速集成</a></p> </div> <div class="jumbotron grayJumbotron text-center jumb_4 animate-if"> <h1>社区镜像管理</h1> <p class="descript"> <span class="glyphicon glyphicon-duplicate book-icon"></span><br> 你可以管理自己构建的镜像，以及查看社区维持的镜像，你可以通过这些镜像快速启动你的应用服务。 </p> <p class="link"><a class="btn btn-lg btn-success" ng-href="#/">镜像查看</a></p> </div> <div class="jumbotron whiteJumbotron text-center jumb_5 animate-if"> <h1>社区应用管理</h1> <p class="descript"> <span class="glyphicon glyphicon-console book-icon"></span><br> 社区上通过镜像部署的应用，你可以放心的托管和管理。 </p> <p class="link"><a class="btn btn-lg btn-success" ng-href="#/">我的应用</a></p> </div> <div class="jumbotron blueJumbotron text-center jumb_6 animate-if"> <h1>社区加速器</h1> <p class="descript"> <span class="glyphicon glyphicon-plane book-icon"></span><br> 如果官方下载速度无法满足你下载的要求时，考虑社区加速器，让你的下载杠杠的。 </p> <p class="link"><a class="btn btn-lg btn-success" ng-href="#/">我要加速</a></p> </div> <div class="jumbotron grayJumbotron text-center jumb_7 animate-if"> <h1>参与社区建设</h1> <p class="descript"> <span class="glyphicon glyphicon-map-marker book-icon"></span><br> 社区目前处于建设阶段，需要广大的社区成员加入。<br> Let\'s go！让我们一起来创建更好的社区体验。 </p> <p class="link"><a class="btn btn-lg btn-success" ng-href="#/">加入我们</a></p> </div>')}]);
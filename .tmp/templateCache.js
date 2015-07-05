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

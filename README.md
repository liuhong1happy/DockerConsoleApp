# DockerConsoleApp

DockerConsoleApp目前是由docker社区的爱好者[注：起源docker百度贴吧]发起的开源PAAS项目。期望能开发出一个具备当前通用PAAS平台的特定，又海纳百川融入更多优秀PAAS的特点。如果愿意贡献你的金点子或者你的银键盘，请联系[liuhong1.happy@163.com](mailto:liuhong1.happy@163.com)。

## TODO 列表

- 文档整理：环境搭建、开发文档、需求文档
- 服务发现：识别域名
- 加速器：首个通过平台自测项目
- 线上调试：线上安装部署
- 容器异常提示：提示部署的用户以及开发人员
- 容器流量监控：避免恶意容器，破坏主机
- 代码托管优化：可以在我们的平台直接编写dockerfile并构建镜像运行容器
- 平台健康监测：随时自检，报告各模组的健康状况
- 异步mongo：更换mongdo驱动为motor
- 前端界面优化：更换碍眼的UI设计和色调
- 自动化测试：选择CI工具，对平台代码或者托管的代码库进行自动化测试
- 自动化部署：借用webhooks或者自己开发web回调API接口实现自动化部署

## 技术列表

- 后端开发语言 python 2.7
- 后端开发框架 tornado 4.2.1
- 前端开发框架 angularjs
- 前端脚手架工具 yo
- 前端自动化构建 bower grunt
- 前端自动化测试工具 karma
- docker应用程序接口 docker-py
- session存储 redis
- 服务发现 etcd
- docker中文翻译文档 gitbook
- 代码仓库 gitlab
- 持续集成 gitlab ci(可能会更换为其他方案)
- 自动化部署 docker-py
- 数据库存储 mongodb

## 开发文档和环境安装

请参考[wiki](https://github.com/liuhong1happy/DockerConsoleApp/wiki)，此处略！


# 基础镜像
FROM liuhong1happy/docker-angularjs
# 维护人员
MAINTAINER  liuhong1.happy@163.com
# 添加环境变量
ENV USER_NAME admin
# 安装git
RUN apt-get install -y git
RUN git clone https://github.com/liuhong1happy/DockerConsoleApp /code
RUN cp
# 安装python库
COPY requirements.txt /requirements.txt
RUN  pip install -r /requirements.txt
# 拷贝代码
COPY . /code
WORKDIR /code
RUN npm install && bower install && grunt
# 默认挂载/var/run和/code
VOLUME ["/var/run","/code"]
# 默认暴露80端口
EXPOSE 80
# 配置supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# 启动supervisord
CMD ["/usr/bin/supervisord"]

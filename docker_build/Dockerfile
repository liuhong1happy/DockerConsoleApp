# 基础镜像
FROM liuhong1happy/docker-angularjs
# 维护人员
MAINTAINER  liuhong1.happy@163.com
# 添加环境变量
ENV USER_NAME admin
ENV SERVICE_ID console
# 安装git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/* 
RUN git clone https://github.com/liuhong1happy/DockerConsoleApp /app
# 安装python库
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN cd /app/libs/stormed-amqp/ && python setup.py install
# 拷贝代码
WORKDIR /app
RUN npm install 
RUN bower install --allow-root 
RUN grunt --force
# 默认挂载/var/run和/app
VOLUME ["/var/run","/app"]
# 默认暴露80端口
EXPOSE 80
# 配置supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# 启动supervisord
CMD ["/usr/bin/supervisord"]

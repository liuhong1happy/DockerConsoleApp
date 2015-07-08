import logging 
import docker
from tornado.options import define, options
import settings



def init_docker():
    docker_client = None
    try:
        docker_client = docker.Client(base_url=settings.DOCKER_HOST)
        options.docker_client = docker_client
        logging.info("Init docker client successed")
    except Exception,e:
        logging.error("Init docker client failed",e)

    return docker_client
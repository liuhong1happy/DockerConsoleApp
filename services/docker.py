from tornado.optoins import options,define

class DockerClient():
    def __init__(self):
        self.docker_client = options.docker_client

    def containers(self,all=True,quiet=False,trunc=True,
                   latest=False,since=None,before=None,
                   limit=20,size=True,filters=None,callback=None):
        
        if hasattr(self,"docker_client"):
            callback(self.docker_client.containers(all=all,quiet=quiet,trunc=trunc,
                   latest=latest,since=since,before=before,limit=20,size=size,filters=filters)
        else:
            callback(None)
    
    def images(self,name=None,quiet=True,all=True,filters={ "dangling":True }):
        if hasattr(self,"docker_client"):
            callback(self.docker_client.images(name=name,quiet=quiet,all=all,filters=filters))
        else:
            callback(None)
                     
    def image_info(self,image_id,callback=None):
        if hasattr(self,"docker_client"):
            callback(self.docker_client.inspect_image(image_id=image_id))
        else:
            callback(None)     
                     
    def container_info(self,container,callback=None):
        if hasattr(self,"docker_client"):
            callback(self.docker_client.inspect_image(container=container))
        else:
            callback(None)   
    
    def pull_image(self,name,repository=None,tag=None,stream=False,
                   insecure_registry=False,auth_config=None,callback=None):
        if hasattr(self,"docker_client"):
            callback(self.docker_client.pull(name,repository=repository,tag=tag,stream=stream,
                insecure_registry=insecure_registry,auth_config=auth_config))
        else:
            callback(None) 
        
    def create_container(self, image, command=None, hostname=None, user=None,
                         detach=False, stdin_open=False, tty=False,
                         mem_limit=None, ports=None, environment=None,
                         dns=None, volumes=None, volumes_from=None,
                         network_disabled=False, name=None, entrypoint=None,
                         cpu_shares=None, working_dir=None, domainname=None,
                         memswap_limit=None, cpuset=None, host_config=None,
                         mac_address=None, labels=None, volume_driver=None,callback=None):
                     
        if hasattr(self,"docker_client"):
            callback(
                    self.docker_client.create_container(
                        image, command=command, hostname=hostname, user=user,
                         detach=detach, stdin_open=stdin_open, tty=tty,
                         mem_limit=mem_limit, ports=ports, environment=environment,
                         dns=dns, volumes=volumes, volumes_from=volumes_from,
                         network_disabled=network_disabled, name=name, entrypoint=entrypoint,
                         cpu_shares=cpu_shares, working_dir=working_dir, domainname=domainname,
                         memswap_limit=memswap_limit, cpuset=cpuset, host_config=host_config,
                         mac_address=mac_address, labels=labels, volume_driver=volume_driver
                )
        else:
            callback(None) 
    
                     
    
    
#coding:utf8
import docker


class DockerTools(object):

    def __init__(self):


        # self.client = docker.DockerClient(base_url='tcp://127.0.0.1:2375')
        self.client = docker.from_env()


    @property
    def containers(self):
        '''

        :return:容器对象
        '''
        return self.client.containers

    @property
    def images(self):
        '''

        :return:镜像对象
        '''
        return self.client.images

    def run(self,args):
        '''
        运行容器
        :param args:镜像参数等
        :return: 容器id
        "image": "mysql:1.0.0.1",     镜像名称
        "ports": {'2234': 3306},      端口映射
        "name": "current_mysql",      容器名称
        "environment": {'MYSQL_ROOT_PASSWORD': '123456'},    环境变量参数
        "detach": "True",         是否后台运行
        "volumes": {'/var/docker_file/data': {'bind': '/var/lib/mysql', 'mode': 'rw'}}   挂载数据卷，读写模式
        '''
        return self.containers.run(image=args['image'],
                                   ports=args['ports'],
                                   name=args['name'],
                                   environment=args['environment'],
                                   detach=args['detach'],
                                   volumes=args.get('volumes',None)).id

    def build(self,args):
        '''
        构建新镜像
        :param args:镜像参数
        :return:
        path = './',  docker_file 和当前脚本目录同级就用 ./
        tag = 'mysql:1.0.0.2'  镜像标签
        '''


        # print(res.get(res.list()[0].id).logs())
        return self.images.build(path=args['path'],
                                 tag=args['tag'])


    def get_by_id(self,id):
        '''

        :param id:容器id
        :return: 容器对象
        '''
        return self.containers.get(id)

    def rm(self,id):
        '''
        删除容器
        :param id:容器id
        :return:
        '''
        return self.get_by_id(id).remove()

    def stop(self,id):
        '''
        停止容器
        :param id:容器id
        :return:
        '''
        return self.get_by_id(id).stop()

if __name__ == '__main__':
    current_container = {
        "image":"redis",
        "ports":{'1234': 3306},
        "name":"current_mysql",
        "environment":{'MYSQL_ROOT_PASSWORD': '123456'},
        "detach":"True"
    }
    backup_container = {
        "image": "mysql:1.0.0.1",
        "ports": {'2234': 3306},
        "name": "current_mysql",
        "environment": {'MYSQL_ROOT_PASSWORD': '123456'},
        "detach": "True",
        "volumes": {'/var/docker_file/data': {'bind': '/var/lib/mysql', 'mode': 'rw'}}
    }


    doc = DockerTools()
    # current_container_id = doc.run(backup_container)
    # print(doc.stop(current_container_id))
    doc.stop(self.docker_config['current_container_id'])
    # print(doc.rm(current_container_id))
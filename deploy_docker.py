#coding:utf8
import json,sys
from docker_de import DockerTools



class MysqlDocker(object):
    '''
    调用方式：E:\dev_file\deploy_docker.py deploy 1.0.1 1
    接受3个参数：
    type 部署类型，是发布还是初始化容器  deploy 或 init
    version_no  镜像的版本号   1.0.1版本名称字符串
    new  是否是新镜像标识符    1或0
    '''
    def __init__(self,args):
        self.args = args
        self.docker_config = json.load(open('docker_config.json','r'))
        self.doc = DockerTools()

        self.dockerfile = ['FROM mysql:{0} \n', 'COPY ./data /var/lib/mysql\n']

    def docker_reboot(self):
        doc = self.doc
        if self.docker_config['current_container_id']:
            try:
                print('关闭当前正在运行的容器')
                doc.stop(self.docker_config['current_container_id'])
                print('删除当前容器,容器id为：',self.docker_config['current_container_id'])
                doc.rm(self.docker_config['current_container_id'])
            except Exception as e:
                print(e)
                print('关闭容器失败，或关闭的容器ID不存在')
        print('初始化构建容器')
        if self.args['new']:
            with open('Dockerfile','w') as f:
                self.dockerfile[0] = self.dockerfile[0].format(self.docker_config['docker_version'][-1])
                f.writelines(self.dockerfile)
            print('开始准备构建mysql_docker')
            doc.build(args={'path':'./','tag':'mysql:{0}'.format(self.args['version_no'])})
            self.docker_config['docker_version'].append(self.args['version_no'])
            print(self.docker_config['docker_version'])
            print('构建完成，准备启动当前容器')
            current_container_id = doc.run(args={
                "image":"mysql:{0}".format(self.args['version_no']),
                "ports":{'3306': 9997},
                "name":"current_mysql",
                "environment":{'MYSQL_ROOT_PASSWORD': '123456'},
                "detach":"True"
            })
            self.docker_config['current_container_id'] = current_container_id
            with open('docker_config.json', 'w') as f:
                json.dump(self.docker_config, f)
        else:

            print('已关闭当前容器，准备重启容器')
            if self.args['version_no'] in self.docker_config['docker_version']:
                current_container_id = doc.run(args={
                    "image":"mysql:{0}".format(self.args['version_no']),
                    "ports":{'3306': 9997},
                    "name":"current_mysql",
                    "environment":{'MYSQL_ROOT_PASSWORD': '123456'},
                    "detach":"True"
                })
                print('容器启动完成，准备更新docker_config配置')
                self.docker_config['current_container_id'] = current_container_id
                with open('docker_config.json', 'w') as f:
                    json.dump(self.docker_config, f)
            else:
                print('无法匹配docker_mysql对应版本')

    def init_docker(self):
        doc = self.doc
        self.args['new'] = True
        self.docker_reboot()
        print('启动当前容器完成，准备启动备份容器')
        backup_container_id = doc.run(args={
            "image": "mysql:{0}".format(self.docker_config['docker_version'][-1]),
            "ports": {'3306': 9998},
            "name": "backup_mysql",
            "environment": {'MYSQL_ROOT_PASSWORD': '123456'},
            "detach": "True",
            "volumes": {'/var/docker_file/docker/data': {'bind': '/var/lib/mysql', 'mode': 'rw'}}
        })
        self.docker_config['backup_container_id'] = backup_container_id
        with open('docker_config.json','w') as f:
            json.dump(self.docker_config,f)


def main(action,args):

    if action == 'deploy':
        print('参数：',args)
        run = MysqlDocker(args)
        run.docker_reboot()
    elif action == 'init':
        print('参数：', args)
        run = MysqlDocker(args)
        run.init_docker()
    else:
        print('参数错误',args)



if __name__ == '__main__':
    if len(sys.argv) == 4:
        args = {'version_no': sys.argv[2], 'new': bool(int(sys.argv[3]))}
        main(sys.argv[1],args)
    else:
        print('参数错误')

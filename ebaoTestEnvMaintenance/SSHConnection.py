# _*_coding:utf-8_*_
import configparser
import json

import paramiko,os,time

host1 = {"host": "192.168.8.109", "port": 22, "username": "tester", "pwd": "t@987654321"}

class SSHConnection(object):

    def __init__(self, host_dict):
        self.host = host_dict['host']
        self.port = host_dict['port']
        self.username = host_dict['username']
        self.pwd = host_dict['pwd']
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def run_cmd(self, command):
        """
         执行shell命令,返回字典
        :param command:
        :return:
        """
        print(command)
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        res, err = stdout.read(), stderr.read()
        result = err if err else "正常执行"
        print(result)

    def upload(self, local_path, target_path):
        # 连接，上传
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 上传至服务器 /tmp/test.py
        sftp.put(local_path, target_path)
        # print(os.stat(local_path).st_mode)
        # 增加权限
        # sftp.chmod(target_path, os.stat(local_path).st_mode)
        sftp.chmod(target_path, 0o755)  # 注意这里的权限是八进制的，八进制需要使用0o作为前缀

    def download(self, target_path, local_path):
        # 连接，下载
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 下载至服务器 /tmp/test.py
        sftp.get(target_path, local_path)

    # 销毁
    def __del__(self):
        self.close()

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath('.'))  # 获取当前文件所在目录的上一级目录，即项目所在目录E:\ebaoProject
    configpath = os.path.join(root_dir, "Machine_List.property")
    cf = configparser.ConfigParser()
    # cf.read("E:\ebaoProject\Machine_List.property") # 读取配置文件
    cf.read(configpath)  # 读取配置文件
    # secs = cf.sections()    # 获取文件中所有的section(一个配置文件中可以有多个配置，如数据库相关的配置，邮箱相关的配置，每个section由[]包裹，即[section])，并以列表的形式返回
    # print(secs)
    # options = cf.options("test1_env") # 获取某个section名为Mysql-Database所对应的键
    # print(options)

    items = cf.items("test1_env")  # 获取section名为test1_env所对应的全部键值对
    print(type(items))
    print('items:', end='')
    print(items)

    host = cf.get("test1_env", "host_3.129")  # 获取[test1_env]中host对应的值
    print('host:'+host)
    print(type(json.loads(host)))
    print('host_3.129:', end='')
    print(json.loads(host)['host'])

    for i in range(len(items)):
        a = SSHConnection(json.loads(items[i][1]))
        a.connect()
        a.download('/usr/local/tomcat/tomcat7_jdk1.7_8038/webapps/dub-manage-webapps.war','E:\\workfile')
        a.close()
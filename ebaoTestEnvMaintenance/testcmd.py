# _*_coding:utf-8_*_

import paramiko,os,time

host1 = {"host": "192.168.8.118", "port": 22, "username": "tester", "pwd": "t@987654321"}

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


# unicode_utils.py
# def to_str(bytes_or_str):
#     """
#     把byte类型转换为str
#     :param bytes_or_str:
#     :return:
#     """
#     if isinstance(bytes_or_str, bytes):
#         value = bytes_or_str.decode('utf-8')
#     else:
#         value = bytes_or_str
#     return value



ssh_8_109 = SSHConnection(host1)
ssh_8_109.connect()


#-----------------------客户应用------------------------
# ----------------------1、杀进程-------------------------
ssh_8_109.run_cmd(
    "ps -ef | grep dub-declare-app | grep -v grep | awk '{print $2}' | xargs kill -9")

print("进程已杀")
# time.sleep(2)
os.system("cd /root/.jenkins/workspace/DUB-V2.0\(dub-declare-app\)/dub-declare-app/target/ ;tar -cvf dub-declare-app.tar dub-declare-app;")
print("tar包完成")
# # ----------------------2、备份原来的包到/back目录下-------------------------

# # 先在对应的tomcat目录下创建目录back
ssh_8_109.run_cmd(
    "\cp -rf /server/soft/exchange/deploy/dub-declare-app /server/soft/exchange/bak/")
# # #----------------------3、删除包-------------------------
ssh_8_109.run_cmd(
    "rm -rf /server/soft/exchange/deploy/dub-declare-app")
# # ----------------------4、拷贝Jenkins服务器上的包到tomcat目录下-------------------------
# # 由于FTP目录结构存在中文，需要在window资源管理器里打开FTP并复制路径

ssh_8_109.upload(
    "/root/.jenkins/workspace/DUB-V2.0(dub-declare-app)/dub-declare-app/target/dub-declare-app.tar".decode("utf-8"),
    "/server/soft/exchange/deploy/dub-declare-app.tar".decode("utf-8"))


ssh_8_109.run_cmd(
    "cd /server/soft/exchange/deploy/;tar -xvf /server/soft/exchange/deploy/dub-declare-app.tar")
ssh_8_109.run_cmd(
    "rm -rf /server/soft/exchange/deploy/dub-declare-app.tar")
ssh_8_109.run_cmd(
    "chmod 777 /server/soft/exchange/deploy/dub-declare-app/dub-declare-app.sh")
ssh_8_109.run_cmd(
    "nohup /server/soft/exchange/deploy/dub-declare-app/dub-declare-app.sh 0100 > /server/soft/exchange/deploy/dub-declare-app/start.log 2>&1 &")

#-----------------------客户应用------------------------

ssh_8_109.close()

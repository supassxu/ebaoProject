# _*_coding:utf-8_*_
import datetime
from ftplib import FTP
import numpy as np
import paramiko


class PutAppToFtpServer:
    """
    1、获取那些应用需要部署；
    2、获取到应用包到应用程序本地；（预先配置好对应的应用从哪里取包）
    3、在FTP服务器上面建好需要部署应用文件夹；
    4、把获取到的应用分发到FTP服务器上；
    """
    global desdir, port, username, pwd, localdir, ftp, app_dir, app_desdir
    # datepath = datetime.datetime.now().strftime('%y-%m-%d').replace('-', '')
    # desdir = "/package/B-报关服务平台2.0/" + datepath + "/"
    desdir = "/package/B-报关服务平台2.0/201129/"
    localdir = "/home/workspace/Application/"
    port = 22
    username = "tester"
    pwd = "t@987654321"
    # 存放包对应的服务器路径的数组
    app_dir = np.array([["dub-manage-webapps", "192.168.3.129",
                         "/usr/local/tomcat/tomcat7_jdk1.7_8038/webapps/dub-manage-webapps.war",
                         "dub-manage-webapps.war"],
                        ["dub-webapps-yb", "192.168.8.27",
                         "/usr/local/tomcat/tomcat7_jdk1.7_7203_dub_webapps_yb/webapps/dub-webapps-yb.war",
                         "dub-webapps-yb.war"],
                        ["dub-dubbo-bill-check", "192.168.3.129",
                         "/usr/local/tomcat/dub-dubbo-bill-check-1.0.1-SNAPSHOT-assembly.tar.gz",
                         "dub-dubbo-bill-check-1.0.1-SNAPSHOT-assembly.tar.gz"],
                        ["dub-openapi", "192.168.3.228",
                         "/usr/local/tomcat/tomcat8_jdk1.8_8200_DUBAPI/webapps/dub-openapi.war", "dub-openapi.war"],
                        ["dub-exchange", "192.168.3.228",
                         "/usr/local/tomcat/dub-exchange/dub-exchange-1.0.1-SNAPSHOT-assembly.tar.gz",
                         "dub-exchange-1.0.1-SNAPSHOT-assembly.tar.gz"],
                        ["dub-examine-north-webapp", "192.168.3.228",
                         "/usr/local/tomcat/tomcat8_jdk1.8_8202_DUB_EXAMINE_CENTER/webapps/dub-examine-north-webapp.war",
                         "dub-examine-north-webapp.war"],
                        ["dub-upload", "192.168.3.228",
                         "/usr/local/tomcat/tomcat7_jdk1.7_7204_UPLOAD/webapps/dub-upload.war", "dub-upload.war"],
                        ["dub-webapps", "192.168.3.228",
                         "/usr/local/tomcat/tomcat7_jdk1.7_7205_DUB_WEBAPPS/webapps/dub-webapps.war",
                         "dub-webapps.war"],
                        ["dub-baseparam-webapp", "192.168.3.228",
                         "/usr/local/tomcat/tomcat7_jdk1.7_7206_BASEPARAM/webapps/dub-baseparam-webapp.war",
                         "dub-baseparam-webapp.war"],
                        ["dub-receipt-handler", "192.168.3.228",
                         "/usr/local/tomcat/dub-receipt-handler/dub-receipt-handler-1.0.1-SNAPSHOT-assembly.tar.gz",
                         "dub-receipt-handler-1.0.1-SNAPSHOT-assembly.tar.gz"],
                        ["dub-dleybsl-webapp", "192.168.8.27",
                         "/usr/local/tomcat/tomcat7_jdk1.7_7200_dub_dleybsl_webapp/webapps/dub-dleybsl-webapp.war",
                         "dub-dleybsl-webapp.war"],
                        ["dub-dlfreight-webapp", "192.168.8.27",
                         "/usr/local/tomcat/tomcat7_jdk1.7_7201_dub_dlfreight_webapp/webapps/dub-dlfreight-webapp.war",
                         "dub-dlfreight-webapp.war"],
                        ["dub-exchange-edl-webapp", "192.168.8.27",
                         "/usr/local/tomcat/tomcat7_jdk1.7_7202_dub_exchange_edl_webapp/webapps/dub-exchange-edl-webapp.war",
                         "dub-exchange-edl-webapp.war"],
                        ["dub-manifest-sz-tools-webapp", "192.168.8.64",
                         "/usr/local/tomcat/dub-manifest-sz-tools-service/dub-manifest-sz-tools-service-1.0.1-SNAPSHOT-assembly.tar.gz",
                         "dub-manifest-sz-tools-service-1.0.1-SNAPSHOT-assembly.tar.gz"],
                        ["dub-hezhu-webapp", "192.168.8.64",
                         "/usr/local/tomcat/tomcat8_jdk1.8_8201_dub_hezhu_mutiproject_webapp/webapps/dub-hezhu-webapp.war",
                         "dub-hezhu-webapp.war"],
                        ["dub-manifest-sz-webapp", "192.168.8.64",
                         "/usr/local/tomcat/tomcat8_jdk1.8_8200_dub_manifest_sz_mutiproject_webapp/webapps/dub-manifest-sz-webapp.war",
                         "dub-manifest-sz-webapp.war"],
                        ["dub-szeybsl-webapp", "192.168.8.64",
                         "/usr/local/tomcat/tomcat8_jdk1.8_8202_dub-szeybsl/webapps/dub-szeybsl-webapp.war",
                         "dub-szeybsl-webapp.war"],
                        ["dub-exchange-esz-webapp", "192.168.8.64",
                         "/usr/local/tomcat/tomcat7_jdk1.7_7203_dub_exchange_eport_sz/webapps/dub-exchange-esz-webapp.war",
                         "dub-exchange-esz-webapp.war"],
                        ["dub-front-end", "192.168.8.113", "/usr/local/tomcat/prod-dub-webapp-index/dist_sz.tar",
                         "dist_sz.tar"],
                        ["dub-front-end-nb", "192.168.3.129", "/usr/local/tomcat/prod-dub-front-end-nb/dist_nb.tar",
                         "dist_nb.tar"],
                        ["dub-front-end-sh", "192.168.3.129", "/usr/local/tomcat/prod-dub-front-end-sh/dist_sh.tar",
                         "dist_sh.tar"],
                        ["dub-front-end-dl", "192.168.3.129", "/usr/local/tomcat/prod-dub-front-end-dl/dist_dl.tar",
                         "dist_sh.tar"],
                        ["phx-operate-front", "192.168.8.113",
                         "/usr/local/tomcat/prod-phx-operate-front/phx-operate-front.tar", "phx-operate-front.tar"],
                        ["phx-operate-app", "192.168.8.109", "/server/soft/exchange/deploy/phx-operate-app/",
                         "phx-operate-app.tar"],
                        ["dub-finance-app", "192.168.8.27", "/server/soft/exchange/deploy/dub-finance-app/",
                         "dub-finance-app.tar"],
                        ["dub-import-controller-app", "192.168.8.94",
                         "/server/soft/exchange/deploy/dub-import-controller-app/", "dub-import-controller-app.tar"],
                        ["dub-import-declare-app", "192.168.8.94",
                         "/server/soft/exchange/deploy/dub-import-declare-app/", "dub-import-declare-app.tar"],
                        ["dub-knowledge-app", "192.168.8.94", "/server/soft/exchange/deploy/dub-knowledge-app/",
                         "dub-knowledge-app.tar"],
                        ["dub-custom-receipt-app", "192.168.8.94",
                         "/server/soft/exchange/deploy/dub-custom-receipt-app/", "dub-custom-receipt-app.tar"],
                        ["dub-customer-app", "192.168.8.94", "/server/soft/exchange/deploy/dub-customer-app/",
                         "dub-customer-app.tar"],
                        ["dub-declare-app", "192.168.8.109", "/server/soft/exchange/deploy/dub-declare-app/",
                         "dub-declare-app.tar"],
                        ["dub-declare-controller", "192.168.8.109",
                         "/server/soft/exchange/deploy/dub-declare-controller/", "dub-declare-controller.tar"],
                        ["dub-declare-qd-app", "192.168.8.109", "/server/soft/exchange/deploy/dub-declare-qd-app/",
                         "dub-declare-qd-app.tar"],
                        ["dub-urule-app", "192.168.8.94", "/server/soft/exchange/deploy/dub-urule-app/",
                         "dub-urule-app.tar"],
                        ["dub-bill-distribution-app", "192.168.8.109",
                         "/server/soft/exchange/deploy/dub-bill-distribution-app/", "dub-bill-distribution-app.tar"],
                        ["dub-param-app", "192.168.8.109", "/server/soft/exchange/deploy/dub-param-app/",
                         "dub-param-app.tar"],
                        ["dub-declare-aeo-controller", "192.168.8.12",
                         "/server/soft/exchange/deploy/dub-declare-aeo-controller/", "dub-declare-aeo-controller.tar"],
                        ["dub-declare-aeo-service", "192.168.8.12",
                         "/server/soft/exchange/deploy/dub-declare-aeo-service/", "dub-declare-aeo-service.tar"],
                        ["dub-exchange-aliyun", "192.168.8.27", "/server/soft/exchange/deploy/dub-exchange-aliyun/",
                         "dub-exchange-aliyun.tar"],
                        ["dub-exchange-eport-qd", "192.168.8.109",
                         "/usr/local/tomcat/tomcat7_jdk1.7_7200_dub_exchange_eqd_webapp/webapps/dub-exchange-eqd-webapp.war",
                         "dub-exchange-eqd-webapp.war"],
                        ["dub-flow-app", "192.168.8.94", "/server/soft/exchange/deploy/dub-flow-app/",
                         "dub-flow-app.tar"],
                        ["dub-mobile", "192.168.3.129",
                         "/usr/local/tomcat/tomcat7_jdk1.7_7205_dub_mobile/webapps/dub-mobile.war", "dub-mobile.war"],
                        ["dub-points-webapp", "192.168.3.129",
                         "/usr/local/tomcat/tomcat7_jdk1.7_7209_dub_points/webapps/dub-points-webapp.war",
                         "dub-points-webapp.war"],
                        ["dub-webapp-datas", "192.168.3.129", "/usr/local/tomcat/prod-dub-webapp-datas/dist_datas.tar",
                         "dist_datas.tar"],
                        ["dub-portal-html", "192.168.3.129", "/usr/local/static/dub-portal-html/dist_menhu.tar",
                         "dist_menhu.tar"],
                        ["dub-portal-webapp", "192.168.3.129",
                         "/usr/local/tomcat/tomcat7_jdk1.7_8088/webapps/dub-portal-webapp.war",
                         "dub-portal-webapp.war"],
                        ["dub-dfs", "192.168.8.27", "/usr/local/tomcat/dfs-service-7210/dfs-service-1.0.0-SNAPSHOT.jar",
                         "dfs-service-1.0.0-SNAPSHOT.jar"],
                        ["dub-user-app", "192.168.8.109", "/server/soft/exchange/deploy/dub-user-app/",
                         "dub-user-app.tar"],
                        ])

    def __init__(self, app_list):
        self.app_list = app_list

    def CopyAppToLocal(self, app_dir):
        for i in range(app_dir.shape[0]):
            if app_dir[i][0] in self.app_list:
                ssh_x = PutAppToFtpServer.SSHConnection(
                    {"host": app_dir[i][1], "port": 22, "username": "tester", "pwd": "t@987654321"})
                ssh_x.connect()
                print("应用应用" + app_dir[i][0] + "开始拷贝中；")
                if (app_dir[i][0] == "dub-manage-webapps" or app_dir[i][0] == "dub-webapps-yb" or app_dir[i][0] ==
                        "dub-dubbo-bill-check" or app_dir[i][0] == "dub-openapi" or app_dir[i][0] == "dub-exchange" or
                        app_dir[i][0] == "dub-examine-north-webapp" or app_dir[i][0] == "dub-upload"
                        or app_dir[i][0] == "dub-webapps" or app_dir[i][0] == "dub-baseparam-webapp"
                        or app_dir[i][0] == "dub-receipt-handler" or app_dir[i][0] == "dub-manifest-sz-tools-webapp"
                        or app_dir[i][0] == "dub-dleybsl-webapp" or app_dir[i][0] == "dub-dlfreight-webapp" or
                        app_dir[i][0] == "dub-exchange-edl-webapp" or app_dir[i][0] == "dub-manifest-sz-tools" or
                        app_dir[i][0] == "dub-hezhu-webapp" or app_dir[i][0] == "dub-manifest-sz-webapp" or
                        app_dir[i][0] == "dub-szeybsl-webapp" or app_dir[i][0] == "dub-exchange-esz-webapp" or
                        app_dir[i][0] == "dub-front-end" or app_dir[i][0] == "dub-front-end-nb" or
                        app_dir[i][0] == "dub-front-end-sh" or app_dir[i][0] == "dub-front-end-dl" or
                        app_dir[i][0] == "phx-operate-front" or app_dir[i][0] == "dub-exchange-eport-qd" or
                        app_dir[i][0] == "dub-mobile" or app_dir[i][0] == "dub-points-webapp" or
                        app_dir[i][0] == "dub-webapp-datas" or app_dir[i][0] == "dub-portal-html" or
                        app_dir[i][0] == "dub-portal-webapp" or app_dir[i][0] == "dub-dfs"):
                    app_local_dir = localdir + app_dir[i][2].split('/')[-1]
                    ssh_x.run_cmd("ls -lh " + app_dir[i][2])
                    ssh_x.download(app_dir[i][2], app_local_dir)
                else:
                    ssh_x.run_cmd("cd " + app_dir[i][2] + ";ls -lh;tar -cvf " + app_dir[i][0] + ".tar lib *.sh;")
                    ssh_x.download(app_dir[i][2] + app_dir[i][0] + ".tar", localdir + app_dir[i][0] + ".tar")
                    ssh_x.run_cmd("cd " + app_dir[i][2] + ";rm -rf " + app_dir[i][0] + ".tar;")
                ssh_x.close()
                print("应用应用" + app_dir[i][0] + "拷贝到本地路径成功；")

    def FtpMkdirfolder(self, ftp, app_list1):
        try:
            ftp.cwd(desdir)
            # ftp.mkd("部署说明")
            # ftp.mkd("数据库脚本")
            print("当日版本文件夹已存在，部署说明和数据库脚本文件夹创建成功")
        except:
            ftp.mkd(desdir)
            # ftp.mkd("部署说明")
            # ftp.mkd("数据库脚本")
            print("当日版本文件夹已创建成功，部署说明和数据库脚本文件夹创建成功")
            ftp.cwd(desdir)
        for app in app_list1:
            try:
                ftp.cwd(desdir + str(app))
                print(str(app) + ": 当日版本文件夹已存在")
            except:
                ftp.mkd(app)
                print(str(app) + "：文件夹创建成功")
        print("当日版本所有文件夹创建成功")

    def CopyAppToFtp(self, app_list2, app):
        for i in range(app.shape[0]):
            if app[i][0] in app_list2:
                print("开始上传应用包：" + app[i][3])
                self.FtpUpload(localdir + app[i][3], desdir + app[i][0] + "/" + app[i][3])
                print("应用包：" + app[i][3] + "上传成功")

    def FtpUpload(self, appdir, desdir1):
        # ftp.getwelcome()  # 返回欢迎信息
        # ftp.cwd(desdir)  # 进入远程目录
        bufsize = 1024  # 设置的缓冲区大小
        # 使用二进制的方式打开文件
        f1 = open(appdir, 'rb')
        # 上传文件, bufsize缓冲区大小
        ftp.storbinary("STOR {}".format(desdir1), f1, bufsize)
        f1.close()
        ftp.set_debuglevel(0)  # 关闭调试模式

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
            result = err if err else res
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
    ftp = FTP()  # FTP对象
    ftp.encoding = "gbk"
    ftp.set_debuglevel(0)  # 打开调试级别2，显示详细信息
    ftp.connect("192.168.1.59", 21)  # 连接的ftp sever和端口
    ftp.login("dongye", "t@12345678")  # 连接的用户名，密码

    """all_app_list = ["dub-manage-webapps","dub-webapps-yb","dub-dubbo-bill-check","dub-openapi","dub-exchange",
                    "dub-examine-north-webapp","dub-upload","dub-webapps","dub-baseparam-webapp","dub-receipt-handler",
                    "dub-dleybsl-webapp","dub-dlfreight-webapp","dub-exchange-edl-webapp",
                    "dub-manifest-sz-tools-webapp","dub-hezhu-webapp","dub-manifest-sz-webapp","dub-szeybsl-webapp",
                    "dub-exchange-esz-webapp","dub-front-end","dub-front-end-nb","dub-front-end-sh","dub-front-end-dl",
                    "phx-operate-front","phx-operate-app","dub-finance-app","dub-import-controller-app",
                    "dub-import-declare-app","dub-knowledge-app","dub-custom-receipt-app","dub-customer-app",
                    "dub-declare-app","dub-declare-controller","dub-declare-qd-app","dub-urule-app",
                    "dub-bill-distribution-app","dub-param-app","dub-declare-aeo-controller","dub-declare-aeo-service",
                    "dub-exchange-aliyun","dub-exchange-eport-qd","dub-flow-app","dub-mobile","dub-points-webapp",
                    "dub-webapp-datas","dub-portal-html","dub-portal-webapp","dub-dfs"] """

    app_list_test = ["dub-finance-app", "dub-import-controller-app", "dub-import-declare-app", "dub-declare-aeo-controller", "dub-declare-aeo-service", "dub-declare-app", "dub-declare-qd-app", "dub-szeybsl-webapp", "dub-front-end", "dub-front-end-nb", "dub-hezhu-webapp", "dub-webapp-datas", "dub-baseparam-webapp", "dub-user-app", "dub-declare-controller", "dub-front-end-sh"]
    p = PutAppToFtpServer(app_list_test)
    #p.CopyAppToLocal(app_dir)
    #p.FtpMkdirfolder(ftp, app_list_test)
    p.CopyAppToFtp(app_list_test, app_dir)
    ftp.close()
    print("应用从测试环境发送到FTP服务器（192.168.1.59）机器成功，请核对相应的应用存放情况！")
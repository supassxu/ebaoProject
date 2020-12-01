# _*_coding:utf-8_*_
import datetime
import os
from ftplib import FTP
import numpy as np
import paramiko
#import testcmd

class PutAppToFtpServer:
    global desdir, port, username, pwd, localdir, ftp, app_dir, app_desdir
    datepath = datetime.datetime.now().strftime('%y-%m-%d').replace('-', '')
    desdir = "/package/B-报关服务平台2.0/" + datepath + "/"
    localdir = "/home/workspace/Application"
    port = 22
    username = "tester"
    pwd = "t@987654321"

    app_dir = np.array([["dub-manage-webapps", "192.168.3.129", "/usr/local/tomcat/tomcat7_jdk1.7_8038/webapps/dub-manage-webapps.war"],
               ["dub-webapps-yb", "192.168.8.27", "/usr/local/tomcat/tomcat7_jdk1.7_7203_dub_webapps_yb/webapps/dub-webapps-yb.war"],
               ["dub-dubbo-bill-check", "192.168.3.129", "/usr/local/tomcat/dub-dubbo-bill-check-1.0.1-SNAPSHOT-assembly.tar.gz"],
               ["dub-openapi", "192.168.3.228", "/usr/local/tomcat/tomcat8_jdk1.8_8200_DUBAPI/webapps/dub-openapi.war"],
               ["dub-exchange", "192.168.3.228", "/usr/local/tomcat/dub-exchange/dub-exchange-1.0.1-SNAPSHOT-assembly.tar.gz"],
               ["dub-examine-north-webapp", "192.168.3.228", "/usr/local/tomcat/tomcat8_jdk1.8_8202_DUB_EXAMINE_CENTER/webapps/dub-examine-north-webapp.war"],
               ["dub-upload", "192.168.3.228", "/usr/local/tomcat/tomcat7_jdk1.7_7204_UPLOAD/webapps/dub-upload.war"],
               ["dub-webapps", "192.168.3.228", "/usr/local/tomcat/tomcat7_jdk1.7_7205_DUB_WEBAPPS/webapps/dub-webapps.war"],
               ["dub-baseparam-webapp", "192.168.3.228", "/usr/local/tomcat/tomcat7_jdk1.7_7206_BASEPARAM/webapps/dub-baseparam-webapp.war"],
               ["dub-receipt-handler", "192.168.3.228", "/usr/local/tomcat/dub-receipt-handler/dub-receipt-handler-1.0.1-SNAPSHOT-assembly.tar.gz"],
               ["dub-dleybsl-webapp", "192.168.8.27", "/usr/local/tomcat/tomcat7_jdk1.7_7200_dub_dleybsl_webapp/webapps/dub-dleybsl-webapp.war"],
               ["dub-dlfreight-webapp", "192.168.8.27", "/usr/local/tomcat/tomcat7_jdk1.7_7201_dub_dlfreight_webapp/webapps/dub-dlfreight-webapp.war"],
               ["dub-exchange-edl-webapp", "192.168.8.27", "/usr/local/tomcat/tomcat7_jdk1.7_7202_dub_exchange_edl_webapp/webapps/dub-exchange-edl-webapp.war"],
               ["dub-manifest-sz-tools", "192.168.8.64", "/usr/local/tomcat/dub-manifest-sz-tools-service/dub-manifest-sz-tools-service-1.0.1-SNAPSHOT-assembly.tar.gz"],
               ["dub-hezhu-webapp", "192.168.8.64", "/usr/local/tomcat/tomcat8_jdk1.8_8201_dub_hezhu_mutiproject_webapp/webapps/dub-hezhu-webapp.war"],
               ["dub-manifest-sz-webapp", "192.168.8.64", "/usr/local/tomcat/tomcat8_jdk1.8_8200_dub_manifest_sz_mutiproject_webapp/webapps/dub-manifest-sz-webapp.war"],
               ["dub-szeybsl-webapp", "192.168.8.64", "/usr/local/tomcat/tomcat8_jdk1.8_8202_dub-szeybsl/webapps/dub-szeybsl-webapp.war"],
               ["dub-exchange-esz-webapp", "192.168.8.64", "/usr/local/tomcat/tomcat7_jdk1.7_7203_dub_exchange_eport_sz/webapps/dub-exchange-esz-webapp.war"],
               ])

    app_desdir = np.array([["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-webapps-yb", "dub-webapps-yb.war", desdir + "dub-webapps-yb/dub-webapps-yb.war"],
                           ["dub-dubbo-bill-check", "dub-dubbo-bill-check-1.0.1-SNAPSHOT-assembly.tar.gz", desdir + "dub-dubbo-bill-check/dub-dubbo-bill-check-1.0.1-SNAPSHOT-assembly.tar.gz"],
                           ["dub-openapi", "dub-openapi.war", desdir + "dub-openapi/dub-openapi.war"],
                           ["dub-exchange", "dub-exchange-1.0.1-SNAPSHOT-assembly.tar.gz", desdir + "dub-exchange/dub-exchange-1.0.1-SNAPSHOT-assembly.tar.gz"],
                           ["dub-examine-north-webapp", "dub-examine-north-webapp.war", desdir + "dub-examine-north-webapp/dub-examine-north-webapp.war"],
                           ["dub-upload", "dub-upload.war", desdir + "dub-upload/dub-upload.war"],
                           ["dub-webapps", "dub-webapps.war", desdir + "dub-webapps/dub-webapps.war"],
                           ["dub-baseparam-webapp", "dub-baseparam-webapp.war", desdir + "dub-baseparam-webapp/dub-baseparam-webapp.war"],
                           ["dub-receipt-handler", "dub-receipt-handler-1.0.1-SNAPSHOT-assembly.tar.gz", desdir + "dub-receipt-handler/dub-receipt-handler-1.0.1-SNAPSHOT-assembly.tar.gz"],
                           ["dub-dleybsl-webapp", "dub-dleybsl-webapp.war", desdir + "dub-dleybsl-webapp/dub-dleybsl-webapp.war"],
                           ["dub-manifest-sz-tools", "dub-manifest-sz-tools-service-1.0.1-SNAPSHOT-assembly.tar.gz", desdir + "dub-manifest-sz-tools/dub-manifest-sz-tools-service-1.0.1-SNAPSHOT-assembly.tar.gz"],
                           ["dub-hezhu-webapp", "dub-hezhu-webapp.war", desdir + "dub-hezhu-webapp/dub-hezhu-webapp.war"],
                           ["dub-manifest-sz-webapp", "dub-manifest-sz-webapp.war", desdir + "dub-manifest-sz-webapp/dub-manifest-sz-webapp.war"],
                           ["dub-szeybsl-webapp", "dub-szeybsl-webapp.war", desdir + "dub-szeybsl-webapp/dub-szeybsl-webapp.war"],
                           ["dub-exchange-esz-webapp", "dub-exchange-esz-webapp.war", desdir + "dub-exchange-esz-webapp/dub-exchange-esz-webapp.war"],
                           ])

    def __init__(self, app_list):
        self.app_list = app_list

    def CopyAppToLocal(slef, app_dir):
        for i in range(app_dir.shape[0]):
            if(app_dir[i][0] in slef.app_list):
                if(app_dir[i][0] == "dub-manage-webapps" or app_dir[i][0] == "dub-webapps-yb" or app_dir[i][0] ==
                        "dub-dubbo-bill-check" or app_dir[i][0] == "dub-openapi" or app_dir[i][0] == "dub-exchange" or
                        app_dir[i][0] == "dub-examine-north-webapp" or app_dir[i][0] == "dub-upload" or app_dir[i][0] ==
                        "dub-webapps" or app_dir[i][0] == "dub-baseparam-webapp" or app_dir[i][0] == "dub-receipt-handler"
                        or app_dir[i][0] == "dub-dleybsl-webapp" or app_dir[i][0] == "dub-dlfreight-webapp" or
                        app_dir[i][0] == "dub-exchange-edl-webapp" or app_dir[i][0] == "dub-manifest-sz-tools" or
                        app_dir[i][0] == "dub-hezhu-webapp" or app_dir[i][0] == "dub-manifest-sz-webapp" or
                        app_dir[i][0] == "dub-szeybsl-webapp" or app_dir[i][0] == "dub-exchange-esz-webapp"):
                    slef.connect(app_dir[i][1], port, username, pwd)
                    slef.download(app_dir[i][1], localdir)
                    slef.close()
                else:
                    pass

    def FtpMkdirfolder(self, ftp, app_list):
        try:
            ftp.cwd(desdir)
            ftp.mkd("部署说明")
            ftp.mkd("数据库脚本")
            print("当日版本文件夹已存在，部署说明和数据库脚本文件夹创建成功")
        except:
            ftp.mkd(desdir)
            ftp.mkd("部署说明")
            ftp.mkd("数据库脚本")
            print("当日版本文件夹已创建成功，部署说明和数据库脚本文件夹创建成功")
            ftp.cwd(desdir)
        for app in app_list:
            try:
                ftp.cwd(desdir + str(app))
                print(str(app) + ": 当日版本文件夹已存在")
            except:
                ftp.mkd(app)
                print(str(app) + "：文件夹创建成功")
        print("当日版本所有文件夹创建成功")

    def CopyAppToFtp(slef, app):
        for i in range(app.shape[0]):
            if(app[i][0] in app_list):
                slef.FtpUpload(os.getcwd() + "/Application/" + app[i][1], desdir + str(app) + "/" + app[i][1])

    ftp.quit()  # 退出ftp

    def FtpUpload(slef, appdir, desdir):
        # ftp.getwelcome()  # 返回欢迎信息
        #ftp.cwd(desdir)  # 进入远程目录
        bufsize = 1024  # 设置的缓冲区大小
        # 使用二进制的方式打开文件
        f = open(appdir, 'rb')
        # 上传文件, bufsize缓冲区大小
        ftp.storbinary("STOR {}".format(desdir, f, bufsize))
        f.close()
        ftp.set_debuglevel(0)  # 关闭调试模式

if __name__ == '__main__':
    ftp = FTP()  # FTP对象
    ftp.encoding = "gbk"
    ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
    ftp.connect("192.168.1.59", 21)  # 连接的ftp sever和端口
    ftp.login("dongye", "t@12345678")  # 连接的用户名，密码
    app_list = ["dub-webapps", "dub-openapi", "dub-webapps-yb", "dub-hezhu-webapp", "dub-manage-webapps", "dub-examine-center-north-webapp", "dub-manifest-sz-tools-webapp", "dub-manifest-sz-webapp", "dub-declare-controller", "dub-szeybsl-webapp", "dub-declare-qd-app", "dub-dleybsl-multiproject-webapp", "phx-operate-app", "dub-import-declare", "dub-finance", "dub-import-controller", "dub-front-end", "dub-front-end-nb", "dub-front-end-sh", "dub-front-end-dl", "phx-operate-front"]

    p = PutAppToFtpServer(app_list)
    #p.CopyAppToLocal(app_dir)
    p.FtpMkdirfolder(ftp, app_list)
    #p.CopyAppToFtp(app_list)
    print("应用从测试环境发送到FTP服务器（192.168.1.59）机器成功，请核对相应的应用存放情况！")

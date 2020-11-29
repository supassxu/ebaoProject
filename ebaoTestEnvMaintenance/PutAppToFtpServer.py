# _*_coding:utf-8_*_
import datetime
import os
from ftplib import FTP
import numpy as np
import testcmd

class PutAppToFtpServer:
    datepath = datetime.datetime.now().strftime('%y-%m-%d').replace('-', '')
    desdir = "/package/B-报关服务平台2.0/" + datepath + "/"
    global desdir
    app_dir = [["dub-manage-webapps", "192.168.3.129", "/usr/local/tomcat/tomcat7_jdk1.7_8038/webapps/dub-manage-webapps.war"],
               ["dub-webapps-yb", "192.168.8.27", "/usr/local/tomcat/tomcat7_jdk1.7_7203_dub_webapps_yb/webapps/dub-webapps-yb.war"],
               ["dub-dubbo-bill-check", "192.168.3.129", "/usr/local/tomcat/dub-dubbo-bill-check-1.0.1-SNAPSHOT-assembly.tar.gz"],
               ["dub-openapi", "192.168.3.228", "/usr/local/tomcat/tomcat8_jdk1.8_8200_DUBAPI/webapps/dub-openapi.war"],
               ["dub-exchange", "192.168.3.228", "/usr/local/tomcat/dub-exchange/dub-exchange-1.0.1-SNAPSHOT-assembly.tar.gz"],
               ["dub-examine-north-webapp", "192.168.3.228", "/usr/local/tomcat/tomcat8_jdk1.8_8202_DUB_EXAMINE_CENTER/webapps/dub-examine-north-webapp.war"],
               ["dub-upload", "192.168.3.228", "/usr/local/tomcat/tomcat7_jdk1.7_7204_UPLOAD/webapps/dub-upload.war"],
               ["dub-webapps", "192.168.3.228", "/usr/local/tomcat/tomcat7_jdk1.7_7205_DUB_WEBAPPS/webapps/dub-webapps.war"],
               ["dub-baseparam-webapp", "192.168.3.228", "/usr/local/tomcat/tomcat7_jdk1.7_7206_BASEPARAM/webapps/dub-baseparam-webapp.war"],
               ["dub-receipt-handler", "192.168.3.129", "/usr/local/tomcat/dub-receipt-handler/dub-receipt-handler-1.0.1-SNAPSHOT-assembly.tar.gz"],
               ["dub-dleybsl-webapp", "192.168.3.129", "/usr/local/tomcat/tomcat7_jdk1.7_7200_dub_dleybsl_webapp/webapps/dub-dleybsl-webapp.war"],
               ["dub-dlfreight-webapp", "192.168.3.129", "/usr/local/tomcat/tomcat7_jdk1.7_7201_dub_dlfreight_webapp/webapps/dub-dlfreight-webapp.war"],
               ["dub-exchange-edl-webapp", "192.168.3.129", "/usr/local/tomcat/tomcat7_jdk1.7_7202_dub_exchange_edl_webapp/webapps/dub-exchange-edl-webapp.war"],
               ["dub-manifest-sz-tools", "192.168.8.64", "/usr/local/tomcat/dub-manifest-sz-tools-service/dub-manifest-sz-tools-service-1.0.1-SNAPSHOT-assembly.tar.gz"],
               ["dub-hezhu-webapp", "192.168.8.64", "/usr/local/tomcat/tomcat8_jdk1.8_8201_dub_hezhu_mutiproject_webapp/webapps/dub-hezhu-webapp.war"],
               ["dub-manifest-sz-webapp", "192.168.8.64", "/usr/local/tomcat/tomcat8_jdk1.8_8200_dub_manifest_sz_mutiproject_webapp/webapps/dub-manifest-sz-webapp.war"],
               ["dub-szeybsl-webapp", "192.168.8.64", "/usr/local/tomcat/tomcat8_jdk1.8_8202_dub-szeybsl/webapps/dub-szeybsl-webapp.war"],
               ["dub-exchange-esz-webapp", "192.168.8.64", "/usr/local/tomcat/tomcat7_jdk1.7_7203_dub_exchange_eport_sz/webapps/dub-exchange-esz-webapp.war"],
               ]
    app_desdir = np.array([["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-webapps-yb", "dub-webapps-yb.war", desdir + "dub-webapps-yb/dub-webapps-yb.war"],
                           ["dub-dubbo-bill-check", "dub-dubbo-bill-check-1.0.1-SNAPSHOT-assembly.tar.gz", desdir + "dub-dubbo-bill-check/dub-dubbo-bill-check-1.0.1-SNAPSHOT-assembly.tar.gz"],
                           ["dub-openapi", "dub-openapi.war", desdir + "dub-openapi/dub-openapi.war"],
                           ["dub-exchange", "dub-exchange-1.0.1-SNAPSHOT-assembly.tar.gz", desdir + "dub-exchange/dub-exchange-1.0.1-SNAPSHOT-assembly.tar.gz"],
                           ["dub-examine-north-webapp", "dub-examine-north-webapp.war", desdir + "dub-examine-north-webapp/dub-examine-north-webapp.war"],
                           ["dub-upload", "dub-upload.war", desdir + "dub-upload/dub-upload.war"],
                           ["dub-webapps", "dub-webapps.war", desdir + "dub-webapps/dub-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ["dub-manage-webapps", "dub-manage-webapps.war", desdir + "dub-manage-webapps/dub-manage-webapps.war"],
                           ])
    ftp = FTP()  # FTP对象
    global ftp
    ftp.encoding = "gbk"
    ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
    ftp.connect("192.168.1.59", 21)  # 连接的ftp sever和端口
    ftp.login("dongye", "t@12345678")  # 连接的用户名，密码
    def __init__(self, app_list):
        self.app_list = app_list

    def CopyAppToLocal(slef):
        pass

    def FtpMkdirfolder(self):
        if(ftp.cwd(desdir)):
            ftp.mkd("部署说明")
            ftp.mkd("数据库脚本")
            print("当日版本文件夹已存在，部署说明和数据库脚本文件夹创建成功")
        else:
            ftp.mkd(desdir)
            ftp.mkd("部署说明")
            ftp.mkd("数据库脚本")
            print("当日版本文件夹已创建成功，部署说明和数据库脚本文件夹创建成功")
        ftp.cwd(desdir)
        for app in app_list:
            if(ftp.cwd(desdir + str(app))):
                print("当日版本文件夹已存在")
            else:
                ftp.mkd(app)
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
    app_list = ['dub-manage-webapps']
    p = PutAppToFtpServer(app_list)
    p.CopyAppToLocal(app_list)
    p.FtpMkdirfolder(app_list)
    p.CopyAppToFtp(app_list)
    print("应用从测试环境发送到FTP服务器（192.168.1.59）机器成功，请核对相应的应用存放情况！")

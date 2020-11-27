# _*_coding:utf-8_*_
from ftplib import FTP


class PutAppToFtpServer:
    #app_list = []
    ftp = FTP()  # FTP对象
    ftp.encoding = "utf-8"
    ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
    ftp.connect("192.168.1.59", 21)  # 连接的ftp sever和端口
    ftp.login("dongye", "t@12345678")  # 连接的用户名，密码
    def __init__(self, app_list):
        self.app_list = app_list

    def CopyAppToLocal(slef):
        pass

    def FtpMkdirfolder(self):
        pass

    def CopyAppToFtp(slef, self.app_list):
        ftp.getwelcome()  # 返回欢迎信息
        ftp.cwd("/package/B-报关服务平台2.0/201127/")  # 进入远程目录
        for app in self.app_list:
            f = open("dub-manage-webapps.war", 'rb')
            # 上传文件, bufsize缓冲区大小
            ftp.storbinary("STOR {}".format("dub-manage-webapps.war"), f, bufsize)
            f.close()
            ftp.set_debuglevel(0)  # 关闭调试模式
            ftp.quit()  # 退出ftp



if __name__ == '__main__':
    app_list = ['','','','']
    p = PutAppToFtpServer(app_list)
    p.CopyAppToLocal(app_list)
    p.FtpMkdirfolder(app_list)
    p.CopyAppToFtp(app_list)
    print("应用从测试环境发送到FTP服务器（192.168.1.59）机器成功，请核对相应的应用存放情况！")
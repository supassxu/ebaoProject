# _*_coding:utf-8_*_
from ftplib import FTP


class PutAppToFtpServer:
    app_list = []
    global app_list
    ftp = FTP()  # FTP对象
    global ftp
    ftp.encoding = "gbk"
    ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
    ftp.connect("192.168.1.59", 21)  # 连接的ftp sever和端口
    ftp.login("dongye", "t@12345678")  # 连接的用户名，密码
    def __init__(self, app_list):
        self.app_list = app_list
        self.ftp = ftp

    def CopyAppToLocal(slef):
        pass

    def FtpMkdirfolder(self):
        pass

    def CopyAppToFtp(slef, app_list):
        for app in app_list:
            FtpUpload(app,os.getcwd() + "",)


def FtpUpload(app,appdir, desdir):
    ftp = FTP()  # FTP对象
    ftp.encoding = "gbk"
    ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
    ftp.connect("192.168.1.59", 21)  # 连接的ftp sever和端口
    ftp.login("dongye", "t@12345678")  # 连接的用户名，密码

    # ftp.getwelcome()  # 返回欢迎信息
    ftp.cwd(desdir)  # 进入远程目录
    bufsize = 1024  # 设置的缓冲区大小
    # 使用二进制的方式打开文件
    f = open(appdir, 'rb')
    # 上传文件, bufsize缓冲区大小
    ftp.storbinary("STOR {}".format(str(app)), f, bufsize)
    f.close()
    ftp.set_debuglevel(0)  # 关闭调试模式
    ftp.quit()  # 退出ftp

if __name__ == '__main__':
    app_list = ['dub-manage-webapps']
    p = PutAppToFtpServer(app_list)
    p.CopyAppToLocal(app_list)
    p.FtpMkdirfolder(app_list)
    p.CopyAppToFtp(app_list)
    print("应用从测试环境发送到FTP服务器（192.168.1.59）机器成功，请核对相应的应用存放情况！")
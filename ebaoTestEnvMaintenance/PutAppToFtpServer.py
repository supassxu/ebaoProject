# _*_coding:utf-8_*_

class PutAppToFtpServer:

    def __init__(self, app_list):
        self.app_list = app_list

    def CopyAppToLocal(slef):
        pass

    def FtpMkdirfolder(self):
        pass

    def CopyAppToFtp(slef):
        pass


if __name__ == '__main__':
    app_list = ['','','','']
    p = PutAppToFtpServer(app_list)
    p.CopyAppToLocal(app_list)
    p.FtpMkdirfolder(app_list)
    p.CopyAppToFtp(app_list)
    print("应用从测试环境发送到FTP服务器（192.168.1.59）机器成功，请核对相应的应用存放情况！")
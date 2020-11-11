# coding=utf-8
from ftplib import FTP
import time, tarfile, os

from ftplib import FTP
class MyFTP():
    def __init__(self,host, port,username, password):
        ftp_ = FTP()
        self.bufsize = 2048
        ftp_.connect(host,port)
        ftp_.login(username,password)
        print("登录成功")
        self.ftp=ftp_

    #从ftp下载文件
    def downloadfile(self, remotepath, localpath):
        with open(localpath, 'wb') as fp:
            self.ftp.retrbinary('RETR ' + remotepath, fp.write, self.bufsize)
            self.ftp.set_debuglevel(0)

    #从本地上传文件到ftp
    def uploadfile(self, remotepath, localpath):
        with open(localpath, 'rb') as fp:
            self.ftp.storbinary('STOR ' + remotepath, fp, self.bufsize)
            self.ftp.set_debuglevel(0)

    def get_file_list(self,path="web/images"):
        # 包含文件名的生成器
        for file in self.ftp.nlst(path):
            yield file

# 单例模式
#myftp = MyFTP("192.168.110.48",21, "Administrator", "liupan@0722")
myftp = MyFTP("192.168.110.48",21, "test", "love!@#110911043")
# 通过myftp.ftp获得ftp对象

if __name__ == "__main__":
    with myftp.ftp:
        # remotepath参数是远程服务器的目录绝对路径
        myftp.downloadfile(remotepath="/a/a.txt", localpath="E:\\supassxu")
        #调用本地播放器播放下载的视频
        #ftp.nlst()  # 获取目录下的文件
        print(myftp.get_file_list())
        print('web/images/2.jpg' in myftp.get_file_list())
        print('web/images/2.jpg' in myftp.get_file_list())
        myftp.uploadfile(remotepath="/a.csv", localpath="C:\DownLoad\\a.csv")
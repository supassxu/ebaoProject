#coding=utf-8
#ftp登陆连接
import datetime
import os
from ftplib import FTP  # 加载ftp模块
#def FTPUpload(appdir,desdir):
ftp = FTP()  # FTP对象
ftp.encoding="gbk"
ftp.set_debuglevel(0)  # 打开调试级别2，显示详细信息
ftp.connect("192.168.1.59", 21)  # 连接的ftp sever和端口
ftp.login("dongye", "t@12345678")  # 连接的用户名，密码
app_list = ['dub-manage-webapps']
#ftp.connect("192.168.110.48", 21)  # 连接的ftp sever和端口
#ftp.login("test", "love!@#110911043")  # 连接的用户名，密码
datepath = datetime.datetime.now().strftime('%y-%m-%d').replace('-', '')
desdir = "/package/B-报关服务平台2.0/" + datepath + "/"
ftp.getwelcome()  # 返回欢迎信息
# ftp.cwd("/package/B-报关服务平台2.0/201127/")  # 进入远程目录
#ftp.nlst("/a")
#bufsize = 1024  # 设置的缓冲区大小
#filename = "abc.txt"  # 需要下载的文件
#file_handle = open(filename, "wb").write  # 以写模式在本地打开文件
#ftp.retrbinaly("RETR %s"%filename, file_handle, bufsize)  # 接收服务器上文件并写入本地文件
# 使用二进制的方式打开文件
#f = open("dub-manage-webapps.war", 'rb')
# 上传文件, bufsize缓冲区大小
#ftp.storbinary("STOR {}".format("dub-manage-webapps.war"), f, bufsize)
#f.close()
print(desdir)
if (ftp.cwd(desdir)):
    print("当日版本文件夹已存在")
else:
    ftp.mkd(desdir)
    print("当日版本文件夹已创建")
ftp.cwd(desdir)
ftp.mkd("部署说明")
ftp.mkd("数据库脚本")
print("部署说明和数据库脚本创建成功")
for app in app_list:
    ftp.mkd(app)
    print(str(app) + "创建成功")


ftp.set_debuglevel(0)  # 关闭调试模式
ftp.quit()  # 退出ftp
# pathname = os.getcwd()


# ftp相关命令操作
'''ftp.cwd(pathname)  # 设置FTP当前操作的路径
ftp.dir()  # 显示目录下所有目录信息
ftp.nlst()  # 获取目录下的文件
ftp.mkd(pathname)  # 新建远程目录
ftp.pwd()  # 返回当前所在位置
dirname = '/a'
filename1 = 'a.txt'
ftp.rmd(dirname)  # 删除远程目录
ftp.delete(filename1)  # 删除远程文件
ftp.rename('b.txt', 'a.txt')  # 将fromname修改名称为toname。
#ftp.storbinaly("STOR filename.txt", file_handel, bufsize)  # 上传目标文件
#ftp.retrbinary("RETR filename.txt", file_handel, bufsize)  # 下载FTP文件
'''
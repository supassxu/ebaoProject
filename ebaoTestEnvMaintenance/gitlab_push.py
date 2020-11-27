import gitlab, time
from dub_script.logging_manage import my_log

logger = my_log("gitlab_push")
url = 'http://192.168.8.79:8081/'
token = 'fJirgXn1e9GuDk8t-YCn'

# 登录
gl = gitlab.Gitlab(url, token)

dec_message = str(time.localtime().tm_year) + "年" + str(time.localtime().tm_mon) + "月" + str(
    time.localtime().tm_mday) + "日发布"


class gitlab_operation(object):
    def __init__(self):
        self.merge_tag = False

    def gitlab_merge(self, project_name, merge_tile):
        # 根据id获得project对象
        project = gl.projects.get(app_dic[project_name])

        # 创建一个merge request
        try:
            mr = project.mergerequests.create({'source_branch': 'test',
                                               'target_branch': 'master',
                                               'title': merge_tile, })

            # 更新一个merge request 的描述
            mr.description = merge_tile
            mr.save()
            time.sleep(0.2)
            mr.merge()
            time.sleep(0.2)

        except Exception as e:
            logger.error(project_name + "出现错误，错误如下：\n" + str(e))
            self.merge_tag = False
        else:
            logger.info(project_name + "合并成功，合并标题为：" + merge_tile)
            self.merge_tag = True
        # 1表示合并成功，可以后续打tag，0则表示合并失败，后续不打tag
        return self.merge_tag

    def gitlab_tag(self, project_name, tag_description):
        project = gl.projects.get(app_dic[project_name])
        tags = project.tags.list()

        # 如果有历史tag
        if tags:

            # 最后一次 tag 名称, 类似于 tag_20200702_1.0.08 格式
            last_tag_name = tags[0].attributes["name"]

            # 提取 1.0.08，打包的时候 version_num 必定有改变
            version_num = last_tag_name[17:19]
            version_two_num = last_tag_name[15]
            version_three_num = last_tag_name[13]

            # 1.0.99中最后两位要进位
            if int(version_num) == 99:

                # 1.9.99 中第二位也要进位
                if int(version_two_num) == 9:
                    new_tag_name = "tag_" + time.strftime("%Y%m%d") + "_" + str(int(version_three_num) + 1) + ".0.00"

                # 只需要进最后两位, version_two_num拼写进去即可，tag_20200702_1.version_two_num.00
                else:
                    new_tag_name = "tag_" + time.strftime("%Y%m%d") + "_" + version_three_num + "." + str(
                        int(version_two_num) + 1) + ".00"

            # 不用进位，最后两位加1。把version_num拼写进去即可。tag_20200702_1.0.version_num
            else:
                new_tag_name = "tag_" + time.strftime(
                    "%Y%m%d") + "_" + version_three_num + "." + version_two_num + "." + "{0:0>2}".format(
                    int(version_num) + 1)

            tag = project.tags.create({'tag_name': new_tag_name, 'ref': 'master'})
            tag.set_release_description(tag_description)
            logger.info(project_name + "打tag成功" + new_tag_name)

        # 如果第一次打tag
        else:
            new_tag_name = "tag_" + time.strftime("%Y%m%d") + "_1.0.01"
            tag = project.tags.create({'tag_name': new_tag_name, 'ref': 'master'})
            tag.set_release_description(tag_description)
            logger.info(project_name + "打tag成功" + new_tag_name)


if __name__ == "__main__":
    # git工程格式为"app_name":app_dic[project_name]
    app_dic = {

        # 前端
        "dub-front-end-nb": 89,
        "dub-front-end-sh": 98,
        # "dub-front-end-dl":119,
        # "dub-front-end-sz": 90,
        # "dub-portal-html":196,
        "dub-front-end": 60,
        # "dub-app-inspection":274,
        #
        # 深圳后端
        "dub-import-declare": 68,
        "dub-import-controller": 56,
        # "dub-knowledge": 53,
        "dub-finance": 57,
        # "dub-custom-receipt": 55,
        # "dub-flow":54,
        # "dub-manifest-sz-mutiproject":181,
        "dub-hezhu-mutiproject": 187,

        # 大连后端
        "dub-dleybsl-multiproject":193,
        # "dub-dlfreight-mutiproject":194,

        # 公共依赖
        "dub-pojo": 127,
        "dub-common-old": 123,
        "dub-model": 126,
        "dub-common-service": 124,
        "dub-parent":125,

        # yb 老易豹dub-webapp-index
        "dub-webapps-yb": 128,
        "dub-webapps":129,
        "dub-manage-webapps": 131,
        "dub-openapi": 132,
        "dub-examine-center": 184,Dy.714790

        # "dub-dubbo-bill-check": 183,
        # "dub-portal-multiproject": 197,
        "dub-szeybsl-multiproject":179,
        "dub-upload":192,
        # "dub-mobile":303,

        # exchange 包括dub-exchange-aliyun、dub-exchange-aliyun、dub-xml-exchange、dub-xml-exchange、dub-exchange-eport-sz
        # "dub-exchange":182,
        "dub-exchange-old": 130,
        # sw_exchange
        # "dub-web-tools":198,

        # "dub-bill-distribution":256,
        # "dub-customer":174,
        # "dub-export-declare":122,
        # "dub-user":230,
        # "dub-param-controller": 199,
        # "dub-baseparam-multiproject": 188,
        "dub-receipt-handler":309,
        "phx-operate-app":324,
        "dub-urule":323,

        # 青岛
        "dub-declare":299
    }
    gitlab_handle = gitlab_operation()
    for i, j in app_dic.items():
        logger.info("开始处理" + i + str(j) + "项目")
        if gitlab_handle.gitlab_merge(i, dec_message):
            gitlab_handle.gitlab_tag(i, dec_message)
        else:
            logger.info(i + "合并失败，请手动打tag")

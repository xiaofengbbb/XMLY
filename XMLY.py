import os
import sys

import requests
import time
import hashlib
import random
import json

resultJson = []


# 爬取喜马拉雅的音乐的类
class ximalaya(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36"
        }

    def getServerTime(self):
        """
        获取喜马拉雅服务器的时间戳
        :return:
        """
        # 这个地址就是返回服务器时间戳的接口
        serverTimeUrl = "https://www.ximalaya.com/revision/time"
        response = requests.get(serverTimeUrl, headers=self.headers)
        return response.text

    def getSign(self, serverTime):
        """
        生成 xm-sign
        规则是 md5(ximalaya-服务器时间戳)(100以内随机数)服务器时间戳(100以内随机数)现在时间戳
        :param serverTime:
        :return:
        """
        nowTime = str(round(time.time() * 1000))

        sign = str(hashlib.md5("ximalaya-{}".format(serverTime).encode()).hexdigest()) + "({})".format(
            str(round(random.random() * 100))) + serverTime + "({})".format(str(round(random.random() * 100))) + nowTime
        # 将xm-sign添加到请求头中
        self.headers["xm-sign"] = sign
        # return sign

    def getInfos(self, albumId, pageNum, sort, pageSize):
        # 先调用该方法获取xm-sign
        self.getSign(self.getServerTime())
        # 将访问数据接口的参数写好
        params = {
            'albumId': albumId,  # 页面id
            'pageNum': pageNum,
            'sort': sort,
            'pageSize': pageSize,  # 一页有多少数据
        }
        # 喜马拉雅数据接口
        url = "https://www.ximalaya.com/revision/play/album"
        response = requests.get(url, params=params, headers=self.headers)
        response = response.json()
        # infos = json.loads(response.text)
        # print(infos)

        for musicData in response["data"]["tracksAudioPlay"]:
            musicUrl = musicData["src"]
            musicIndex = musicData["index"]

            resultJson.append({
                "musicUrl": musicUrl,
                "musicIndex": musicIndex,
            })
        done = int(pageEndNum * 1 / pageEndNum)
        sys.stdout.write(
            "\r[~][%s%s]获取进度: %s%%" % ('█' * done, ' ' * (pageEndNum - done), float(1 / pageEndNum * 100)))
        sys.stdout.flush()
        time.sleep(1)

        fp = open("result-json-{}.txt".format(albumId), "w+", encoding="UTF-8")
        fp.write(json.dumps(resultJson))
        fp.close()
        # infos = json.loads(response.text)
        # return infos

    def download(self, albumId):
        fp = open("result-json-{}.txt".format(albumId), "r", encoding="UTF-8")
        content = eval(fp.read())

        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) \
                    Gecko/20100101 Firefox/58.0',
            'Referer': 'https://www.ximalaya.com'
        }

        for item in content:
            try:
                with open('./%s.m4a' % str(item["musicIndex"]), 'wb') as f:
                    response = requests.get(url=item["musicUrl"], headers=HEADERS)
                    f.write(response.content)
                    time.sleep(1)
            except:
                print("[-] 出错!, 最后一个下载的内容为%s")
                exit(1)
            else:
                print("\r[~]剩余下载数-> ".format(item["musicIndex"]) + str(item["musicIndex"]), end="")

        fp.close()


if __name__ == '__main__':
    ximalaya = ximalaya()
    albumId = input("[~]请输入albumId号: ")
    pageStartNum = int(input("[~]请输入Page页码: "))
    pageEndNum = pageStartNum
    ximalaya.getInfos(albumId, pageStartNum, pageEndNum, '30')
    ximalaya.download(albumId)
    main = "main.exe -albumId=" + albumId
    r_v = os.system(main)
    print(r_v)

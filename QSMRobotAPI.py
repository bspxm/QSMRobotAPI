#!/usr/bin/env python
# coding=utf-8
# 功能 ：封装量子密信群机器人API
# 日期 ：2024-02-27
# 作者：Filter
# EMAIL:bspxm@163.com
"""
Copyright Filter(bspxm@163.com)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
# 说明：
""" 
 支持纯文本、markdown、图片、文件、图文
 a = wx.WxRobot('1111-222-333-444-55555') #webhook
 a.sendMessage('文本内容')
 a.sendMarkdown('markdown内容')
 a.sendImage('d:/图片.jpg') #图片文件的绝对路径
 a.sendMedia('d:/文件.jpg') #文件的绝对路径

 a.sendNews('[{
               "title" : "中秋节礼品领取",
               "description" : "今年中秋节公司有豪礼相送",
               "url" : "www.qq.com",
               "picurl" : "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
           }]')
"""

import requests
import json
import hashlib
import base64
import os
from PIL import Image


class QSMRobot:
    headers = {"Content-Type": "application/json"}
    req_message = {"code": 1, "message": "请求量子密信失败，请检查网络"}

    def __init__(self, webhook):
        self.post_url = "https://im.zdxlz.com/im-api/v1/webHook/send?key={0}".format(
            webhook
        )
        self.uploadPic_url = "https://im.zdxlz.com/im-api/v1/webHook/uploadAttachment?key={0}&type=1".format(
            webhook
        )
        self.webhook = webhook

    def _req(self, data):
        try:
            # print("发送消息：{0}".format(self.post_url))
            return requests.post(
                self.post_url, data=json.dumps(data), headers=self.headers, timeout=10
            ).json()
        except Exception as e:
            return self.req_message

    # 发送文字消息
    def sendMessage(self, message):
        """
        发送消息

        Args:
            message (str): 要发送的消息内容

        Returns:
            str: 请求结果
        """
        data = {"type": "text", "textMsg": {"content": str(message)}}
        return self._req(data)

    def sendNews(self, message):
        """
        发送新闻消息，不建议使用

        Args:
            message (list): 新闻消息列表

        Returns:
            bool: 请求是否成功
        """
        data = {
            "type": "news",
            "news": {"info": message},
        }
        return self._req(data)

    def sendImage(self, image_path):
        # 检查图片文件是否存在
        if os.path.exists(image_path):
            # 设置请求头
            headers = {"Content-Type": "multipart/form-data"}
            # 构造文件参数
            files = {"file": (image_path, open(image_path, "rb"))}
            # 构造数据参数
            data = {"type": 1}
            # 发送POST请求上传图片
            upfile = requests.post(self.uploadPic_url, files=files, data=data).json()
            # 判断上传结果
            if upfile["code"] == 200:
                # 获取文件ID
                fileId = upfile["content"]["id"]

                # 打开图片文件
                img = Image.open(image_path)
                # 获取图片的宽度和高度
                width, height = img.size
                # 打印图片的宽度和高度
                print(width, height)
                # 构造数据参数
                data = {
                    "type": "image",
                    "imageMsg": {"fileId": fileId, "height": height, "width": width},
                }
                # 发送请求
                return self._req(data)
            else:
                # 打印上传失败信息
                print(upfile["message"])

        else:
            # 图片文件不存在
            self.req_message["errmessage"] = "图片文件不存在"
            return self.req_message

    def sendMedia(self, file_path):
        """
        发送媒体文件

        Args:
            file_path (str): 文件路径

        Returns:
            dict: 返回请求结果
        """
        if os.path.exists(file_path):
            headers = {"Content-Type": "multipart/form-data"}
            (path, filename) = os.path.split(file_path)
            files = {"file": (filename, open(file_path, "rb"))}
            data = {"type": 2}
            upfile = requests.post(self.uploadPic_url, files=files, data=data).json()
            if upfile["code"] == 200:
                fileId = upfile["content"]["id"]

                data = {"type": "file", "fileMsg": {"fileId": fileId}}
                return self._req(data)
            else:
                print(upfile["message"])
        else:
            self.req_message["errmessage"] = "文件不存在"
            return self.req_message

# QSMRobotAPI

量子密信机器人API

# 说明：

```python
#支持纯文本、markdown、图片、文件、图文
a = QSMRobotAPI.QSMRobot('1111-222-333-444-55555') #webhook
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
```

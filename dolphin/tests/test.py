# -*- coding: UTF-8 -*-

from urllib import request

def loadPage():
    # 包含一个请求报头的headers, 发送的请求会附带浏览器身份发送
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/5.0)"}
    # 构造一个请求对象
    req = request.Request("https://www.googleapis.com/books/v1/volumes?q=1", headers=headers)
    # 发送http请求，返回服务器的响应内容
    # response响应是一个类文件对象
    response = request.urlopen(req)
    # 类文件对象支持文件操作的相关方法，比如read()：读取文件所有内容，返回字符串
    return response.read()


if __name__ == "__main__":
    # print __name__
    html = loadPage()
    # 打印字符串，也就是整个网页的源码
    print(html)


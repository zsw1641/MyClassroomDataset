"""
下载AVA动作数据集
2021/10/11:
新增：
    1. 断线重连（等待5秒后尝试重连）
    2. 假如要保存的文件路径不存在，则创建
"""
import os
import time

import requests
from contextlib import closing


# 要读取的txt文件
# txts = ['./ava_file_names_trainval_v2.1.txt', './ava_file_names_test_v2.1.txt']
txts = ['./ava_file_names_test_v2.1.txt', './ava_file_names_trainval_v2.1.txt']
# 文件的链接路径
# urls = ['https://s3.amazonaws.com/ava-dataset/trainval/', 'https://s3.amazonaws.com/ava-dataset/test/']
urls = ['https://s3.amazonaws.com/ava-dataset/test/', 'https://s3.amazonaws.com/ava-dataset/trainval/']
# 要保存的文件路径
# saves = ['AVA_Videos/train', 'AVA_Videos/test']
saves = ['AVA_Videos/test', 'AVA_Videos/train']


def download(txts=txts, urls=urls, saves=saves):
    try:
        # 循环读取文件
        for i in range(len(txts)):
            # 读取文件内容
            with open(txts[i], 'r') as f:
                # 获取所有行
                lines = f.readlines()
                index = 0
                # 判断保存路径是否存在
                if not os.path.exists(saves[i]):
                    os.mkdir(saves[i])
                # 分别读取每一行
                for line in lines:
                    index += 1
                    # url地址拼接
                    url = os.path.join(urls[i], line.rstrip('\n'))
                    # 保存地址
                    savePath = os.path.join(saves[i], line.rstrip('\n'))
                    # 显示文件完整链接
                    print('\n' + url)
                    with closing(requests.get(url, stream=True)) as response:
                        chunk_size = 1024  # 单次请求最大值 1KB
                        content_size = int(response.headers['content-length'])  # 内容体总大小
                        data_count = 0  # 初始进度
                        # 如果文件已经存在，则比对文件大小，
                        if os.path.exists(savePath):
                            print('{} 已存在，将比对文件大小 本地文件: {} - 远程文件: {}'.format(savePath, os.path.getsize(savePath), content_size))
                        # 如果下载完成，则跳过
                        if os.path.exists(savePath) and os.path.getsize(savePath) == content_size:
                            print('{} 已经下载完成，下载下一个文件'.format(savePath))
                            continue
                        with open(savePath, 'wb') as file:
                            # 循环写入
                            for data in response.iter_content(chunk_size=chunk_size):
                                file.write(data)
                                data_count = data_count + len(data)
                                now_jd = (data_count / content_size) * 100
                                # 打印进度条，以MB为单位
                                print("\r {} / {} 文件下载进度：{:.2f}% ({:.2f}MB / {:.2f}MB) - {}".format(index, len(lines), now_jd, data_count/1024/1024, content_size/1024/1024, savePath), end=" ")

            print('全部下载完成！')
    except Exception:
        sleep = 5
        for i in range(sleep):
            print('\r网络中断，{}s后尝试重新下载！'.format(sleep - i), end='')
            time.sleep(1)
        print('\r开始尝试重新下载！', end='')
        download(txts=txts, urls=urls, saves=saves)


download(txts=txts, urls=urls, saves=saves)

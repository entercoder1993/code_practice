import json
import os
from hashlib import md5
import re
import time
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from requests import RequestException
from spider_toutiao.config import *
from multiprocessing import Pool

'''
流程框架：
1. 抓取索引页内容
   利用requests请求目标站点，得到索引网页HTML代码，返回结果
2. 抓取详情页内容
   解析返回结果，得到详情页的链接，并进一步抓取详情页的信息
3. 下载图片与保存数据库
   将图片下载到本地，并把页面信息及图片URL保存至MongoDB
4. 开启循环及多线程
   对多页内容遍历，开启多线程提高抓取速度
'''


def get_page_index(offset,keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页错误')
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def get_page_detail(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页页错误', url)
        return None


def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select("title")[0].get_text()
    images_pattern = re.compile('gallery: JSON.parse\((.*?)\),',re.S)
    results = re.search(images_pattern,html)
    if results:
        data = json.loads(json.loads(results.group(1)))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image,title)
            return {
                'title': title,
                'url': url,
                'images': images
            }


def download_image(url, title):
    print("正在下载：" + title)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content,title)
    except RequestException:
        print('请求图片出错', url)
        return None


def save_image(content, title):
    if not os.path.exists(title):
        os.mkdir(title)
    file_path = '{0}/{1}.{2}'.format(title,md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()


def main():
    for i in range(OFFSET):
        html = get_page_index(20 * i,KEYWORD + '图集')
        for url in parse_page_index(html):
            html = get_page_detail(url)
            time.sleep(1)
            if html:
                parse_page_detail(html,url)


if __name__ == '__main__':
    # groups = [x * 20 for x in range(GROUP_START,GROUP_END + 1)]
    # pool = Pool()
    # pool.map(main, groups)
    main()
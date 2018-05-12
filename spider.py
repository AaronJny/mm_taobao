# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import requests
from bs4 import BeautifulSoup
import json
import os
import logging

# 首页接口地址
index_url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
# 存放图片的主目录
base_path = 'images'
# 下载起始页
start_page = 1
# 下载终止页
end_page = 2
# 单个模特下载的最大图片数
download_limit = 10

# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


def parse_index(page_num, session):
    """
    解析淘女郎首页接口
    :param page_num 要解析第几页
    :return:
    """
    logger.info(u"当前正在解析第{}页...".format(page_num))
    # 设置用于访问的请求头
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://mm.taobao.com',
        'referer': 'https://mm.taobao.com/search_tstar_model.htm',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    # 设置post的数据
    data = {
        'q': '',
        'viewFlag': 'A',
        'sortType': 'default',
        'searchStyle': '',
        'searchRegion': 'city:',
        'searchFansNum': '',
        'currentPage': '{}'.format(page_num),
        'pageSize': '100',
    }
    # 进行请求，并用resp接收返回结果
    resp = session.post(url=index_url, data=data,
                        headers=headers)
    # 将json字符串转换成字典对象
    data = json.loads(resp.content.decode('gbk'))
    # 找到含有淘女郎信息的列表
    data = data['data']['searchDOList']
    for mm in data:
        city = mm['city']
        name = mm['realName']
        userid = mm['userId']
        next_url = 'https://mm.taobao.com/self/aiShow.htm?userId={}'.format(userid)
        parse_mmpage(session, next_url, city, name)


def parse_mmpage(session, url, city, name):
    """
    解析模特主页
    :param session:
    :param url: 需要请求的地址
    :param city: 模特所在的城市
    :param name: 模特的姓名
    :return:
    """
    logger.info(u'正在保存 {}-{} 的图片...'.format(city, name))
    # 检查是否存在base_path目录，不存在则创建
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    # 检测是否存在当前 姓名-城市 的文件夹，不存在则创建
    current_path = os.path.join(base_path, '{}-{}'.format(name, city).encode('gbk'))  # windows下转成了gbk，linux下不需要
    if not os.path.exists(current_path):
        os.mkdir(current_path)
    # 设置请求消息头
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://mm.taobao.com/search_tstar_model.htm',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }
    # 请求页面
    resp = session.get(url=url, headers=headers)
    # 解码
    content = resp.content.decode('gbk')
    # 构建beautifulsoup对象
    bsobj = BeautifulSoup(content, 'lxml')
    # 获取div中所有的img对象
    img_list = bsobj.find('div', {'class': 'mm-aixiu-content', 'id': 'J_ScaleImg'}).find_all('img')
    # 遍历img对象，获得其下载地址
    cnt = 1
    for img in img_list:
        try:
            src = 'http:' + img.get('src')
        except:
            continue
        logger.info(u'正在保存第{}张图片...'.format(cnt))
        cnt += download_img(src, current_path, '{}.jpg'.format(cnt))
        # 每个模特最多只下载download_limit张
        if cnt > download_limit:
            break


def download_img(url, path, name):
    """
    下载一张图片
    :param url: 图片地址
    :param path: 图片保存路径
    :param name: 图片保存名称
    :return:
    """
    # 设置请求头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'img.alicdn.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }
    # 下载图片
    resp = requests.get(url, headers=headers)
    # 舍弃掉太小的图片，它可能是图标
    if len(resp.content) < 1000:
        return 0
    # 将图片以二进制的形式写入到文件中
    with open(os.path.join(path, name), 'wb') as f:
        f.write(resp.content)
    return 1


if __name__ == '__main__':
    # 创建一个session
    session = requests.Session()
    # 从起始页到终止页，逐页抓取
    for x in range(start_page, end_page + 1):
        # 抓取一页
        parse_index(x, session)

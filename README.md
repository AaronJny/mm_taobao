# 抓取淘女郎图片的简单爬虫

这是一个示例爬虫，用于博文[python爬虫入门教程(三)：淘女郎爬虫 ( 接口解析 | 图片下载 )](https://blog.csdn.net/aaronjny/article/details/80291997)的延时与讲解。

此爬虫用于采集淘女郎的图片信息，具有如下功能：

- 可以设定抓取的起始页和终止页，程序会从起始页开始逐页抓取

- 可以设定每个模特抓取的最大图片数，抓取到指定数目后就会跳过

- 为每个淘女郎以“名字-城市”的格式创建文件夹，并将采集到的图片放入对应的文件夹中

更多信息请阅读[博文](https://blog.csdn.net/aaronjny/article/details/80291997)。

********************************

## 快速开始

** 1.运行环境 **

```
python 2.7
requests==2.18.4
beautifulsoup4==4.6.0
lxml==3.8.0
```

** 2.运行 **

安装依赖环境、配置如下信息后，运行`spider.py`即可。

```python
# 存放图片的主目录
base_path = 'images'
# 下载起始页
start_page = 1
# 下载终止页
end_page = 2
# 单个模特下载的最大图片数
download_limit = 10
```
# 喜马拉雅
## 爬虫项目
根据网站的alumbID号获取网页；
根据提示信息输入页码；
先进行爬虫，将index索引号和url链接存储到txt文件中；
从爬取到的txt文件进行多线程下载.m4a格式的音频文件；
## 数据库存储
将爬虫得到的音频文件和索引号存到数据库
连接数据库，在数据库中建立alumbID号的表
将index索引号、url、和本地存储路径存储到数据库中

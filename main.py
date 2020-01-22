from items import wanacg
from pipeline import pipeline
from download import collect_results,download_image_thread
from output import output

def to_db(items):
    pipeline(items)

def to_download(items, basename):  #参数basename控制总路径
    collect_results(items)
    for item in items:
        download_image_thread(item['results'], basename, int(len(item['results'])/12))  #默认路径参数F:\Yel\Manga

def db_to_magnet(num):
    output(num)
    

if __name__ == '__main__':
    items = wanacg().req(5)  #请求并获取将要下载的漫画信息列表items，修改传参修改页数

    # to_db(items)  #爬取并储存到数据库
    to_download(items, 'F:\\Yel\\Manga')  #下载全部爬取对象到F\Yel\Manga
    # db_to_magnet(30)  #从数据库输出指定数量为磁力格式，该功能不需要items输出


    
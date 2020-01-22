# -*-coding: utf-8 -*-
import time,os,json,requests,re
from multiprocessing.pool import ThreadPool
from lxml import etree


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
}
proxies = {
    'http': 'http://localhost:1080',
    'https': 'https://localhost:1080'
}


def collect_results(items):
    
    for item in items:
        response = requests.get(item['gallary'], headers=headers, proxies=proxies, timeout=10)
        match = re.search( r'imglist = [\s\S]*?\ndocument\.writeln', response.text).group()[10:-21]
        match = match.replace("fast_img_host+\\", "").replace("caption: \\", "caption: ").replace("url", "\"url\"").replace("caption", "\"caption\"").replace('[', '').replace(']','').replace('\\','').replace("},{", "}cut{")
        results = match.split('cut')
        item['results'] = []

        for result in results[0:-1]:
            dic = json.loads(result)
            dic['title'] = item['title']
            dic['url'] = 'http:' + dic['url']
            item['results'].append(dic)

def download_image(url, caption, title, basename):
    '''
    根据result（每个漫画的每张图片的对象）下载图片
    '''
    try:
        res = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        if res.status_code == 200:
            f = open(basename + '\\' + title + '\\' + caption + '.jpg', 'wb')
            f.write(res.content)
            f.flush()
            f.close()
            print("download image successfully:{}".format(url))
            return basename + '\\' + title + '\\' + caption + '.jpg'
    except Exception as e:
        print(e)

    print("download image failed:{}".format(url))
    return None


def download_image_thread(results, basename, num_processes, remove_bad=False, Async=True):
    '''
    多线程下载图片
    :param results: 每个漫画的全部图片对象组成的列表
    :param num_processes: 开启线程个数
    :param remove_bad: 是否去除下载失败的数据
    :param Async:是否异步
    :return: 返回图片的存储地址列表
    '''
    
    if not os.path.exists(basename + '\\' + results[0]['title']):
        os.makedirs(basename + '\\' + results[0]['title'])
    else:
        return;

    # 开启多线程
    pool = ThreadPool(processes=num_processes)
    thread_list = []
    for result in results:
        if Async:
            out = pool.apply_async(func=download_image, args=(result['url'], result['caption'], result['title'], 'F:\\Yel\\Manga'))  # 异步
        else:
            out = pool.apply(func=download_image, args=(result['url'], result['caption'], result['title'], 'F:\\Yel\\Manga'))  # 同步
        thread_list.append(out)

    pool.close()
    pool.join()
    # 获取输出结果
    image_list = []
    if Async:
        for p in thread_list:
            image = p.get()  # get会阻塞
            image_list.append(image)
    else:
        image_list = thread_list
    if remove_bad:
        image_list = [i for i in image_list if i is not None]
    return image_list


if __name__ == "__main__":
    items = [
        {
            'title': 'hhahaaha',
            'link': 'https://wnacg.org/photos-index-aid-93163.html',
            'download': 'https://wnacg.org/download-index-aid-93163.html',
            'image': 'http://t3.wnacg.download/data/t/0931/63/15794858417821.jpg',
            'bit': 'http://d4.wnacg.download/down/0932/774847921679af06ac788263f467179c.zip',
            'id': '93163',
            'gallary': 'https://wnacg.org/photos-gallery-aid-93163.html'
        },
    ]
    collect_results(items)
    for item in items:
        print(download_image_thread(item['results'], int(len(item['results'])/12)))

    # results = [{'url': 'http://img2.wnacg.download/data/0931/63/192.jpg', 'caption': '192', 'title': '小nv女'},{'url': 'http://img2.wnacg.download/data/0931/63/190.jpg', 'caption': '190', 'title': '小nv女'},{'url': 'http://img2.wnacg.download/data/0931/63/155.jpg', 'caption': '155', 'title': '小nv女'}]
    

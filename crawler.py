#! encoding:utf-8
import requests
import re
import os
from bs4 import BeautifulSoup


def download_img(url, save_fullname, is_overwirte=False):
    # save a image to local disk
    if os.path.exists(save_fullname) and (not is_overwirte):
        return

    r = requests.get(url)
    if 'image' not in r.headers['Content-Type']:
        raise ValueError('is not image')

    if not os.path.exists(os.path.dirname(save_fullname)):
        os.makedirs(os.path.dirname(save_fullname))

    if r.status_code == 200:
        print '[Download] %s \tto %s' % (url, save_fullname)
        with open(save_fullname , 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def get_img_urls_artical(artical_url):
    # get image url list from a artical
    read_until_str = u'※ 發信站: 批踢踢實業坊(ptt.cc)'
    r = requests.get(artical_url)

    try:
        html_text = r.text[:r.text.index(read_until_str)]
    except ValueError as valerr:
        print 'Maybe 404 - Not Found.'
        return False

    img_pattern = re.compile(
        '"//(i\.imgur\.com\/[\w\/.]+(?:jpg|png))"')
    imgur_pattern = re.compile(
        'a href="(https?:\/\/imgur\.com\/[\w\/]+)"')

    # get each img_url in articals
    img_url_list = []
    for img_url in re.findall(img_pattern, html_text):
        img_url_list.append('https://' + img_url)

    # enter imgur website to search images
    imgur_urls = re.findall(imgur_pattern, html_text)
    for imgur_url in imgur_urls:
        r = requests.get(imgur_url)
        img_url = re.findall(img_pattern, r.text)
        if img_url:
            img_url_list.append('http://%s' % img_url[0])
    return img_url_list


def artical_img_download(artical_url):
    # download all images in a artical
    global save_folder

    img_url_list = get_img_urls_artical(artical_url)
    # download images
    for img_url in img_url_list:
        try:
            download_img(img_url, os.path.join(save_folder,
                         os.path.basename(artical_url) +' ' + os.path.basename(img_url)))
        except ValueError as valerr:
            pass


def page_img_download(url = 'https://www.ptt.cc/bbs/Beauty/index1908.html'):
    # download all images in a index page
    global domain

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    articals = soup.find_all('div', attrs={"class":"title"})

    # each artical
    for art in articals:
        if not art.a:
            continue

        artical_url = domain + art.a['href']
        print 'Title:', art.a.contents[0]
        print 'Url:', artical_url

        artical_img_download(artical_url)

    print '==================================='


def auto_crawler(start_no, end_no):
    # download all images range from start page_no to end page_no
    # https://www.ptt.cc/bbs/Beauty/<no._here>.html
    for i in xrange(start_no, end_no+1):
        url = '%s%s/index%s.html' % (domain, board, str(i))
        print url
        page_img_download(url)


# settings
save_folder = r'D:\pic'
domain = 'https://www.ptt.cc'
board = '/bbs/Beauty'

if __name__ == '__main__':
    # Download image from pages
    auto_crawler(1880, 1889)

    # Download from a artical
    # artical_img_download('https://www.ptt.cc/bbs/Beauty/M.1471066567.A.F66.html')
    pass
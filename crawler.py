#! encoding:utf-8
import requests
import re
import os

from bs4 import BeautifulSoup


def download_img(url, save_fullname, is_overwirte=False):
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
    read_until_str = u'※ 發信站: 批踢踢實業坊(ptt.cc)'
    r = requests.get(artical_url)

    try:
        html_text = r.text[:r.text.index(read_until_str)]
    except ValueError as valerr:
        print 'Maybe 404 - Not Found.'
        return False

    """
    img_pattern = re.compile(
        'a href="(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}\.jpg|www\.[^\s]+\.[^\s]{2,}\.jpg)"')
    """
    img_pattern2 = re.compile(
        '"//(i\.imgur\.com\/[\w\/.]+(?:jpg|png))"')
    # img [$alt=" ]{,7}src="//(i\.imgur\.com\/[\w\/.]+(?:jpg|png))"
    imgur_pattern = re.compile(
        'a href="(https?:\/\/imgur\.com\/[\w\/]+)"')

    # get each img_url in articals
    img_url_list = []
    for img_url in re.findall(img_pattern2, html_text):
        img_url_list.append('https://' + img_url)

    # enter imgur website to search images
    imgur_urls = re.findall(imgur_pattern, html_text)
    for imgur_url in imgur_urls:
        r = requests.get(imgur_url)
        img_url = re.findall(img_pattern2, r.text)
        if img_url:
            img_url_list.append('http://%s' % img_url[0])
    return img_url_list


def artical_img_download(artical_url):
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


def test_get_img_urls_artical():
    # need to enter imgur.com
    img_url_list = get_img_urls_artical('https://www.ptt.cc/bbs/Beauty/M.1470838446.A.47E.html')
    assert img_url_list == ['http://i.imgur.com/QVZU6Gq.jpg']

    img_url_list = get_img_urls_artical('https://www.ptt.cc/bbs/Beauty/M.1470926074.A.FB9.html')
    assert img_url_list == ['http://i.imgur.com/F7rzTjT.jpg']

    # normal cases
    img_url_list = get_img_urls_artical('https://www.ptt.cc/bbs/Beauty/M.1470842030.A.3C0.html')
    assert img_url_list == [u'https://i.imgur.com/AwZKag5.jpg', u'https://i.imgur.com/W3QbWFW.jpg',
                            u'https://i.imgur.com/nrkmWGn.jpg', u'https://i.imgur.com/bo8kVkR.jpg']
    print '[get_img_urls_artical] ok!'

def auto_crawler(start_no, end_no):
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
    auto_crawler(1880, 1889)
    # test_get_img_urls_artical()
    pass
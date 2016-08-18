from crawler import *


def test_get_img_urls_artical():
    # need to enter imgur.com
    url = 'https://www.ptt.cc/bbs/Beauty/M.1470838446.A.47E.html'
    img_url_list = get_img_urls_artical(url)
    assert img_url_list == ['http://i.imgur.com/QVZU6Gq.jpg']

    url = 'https://www.ptt.cc/bbs/Beauty/M.1470926074.A.FB9.html'
    img_url_list = get_img_urls_artical(url)
    assert img_url_list == ['http://i.imgur.com/F7rzTjT.jpg']

    # normal cases
    url = 'https://www.ptt.cc/bbs/Beauty/M.1470842030.A.3C0.html'
    img_url_list = get_img_urls_artical(url)
    assert img_url_list == [u'https://i.imgur.com/AwZKag5.jpg',
                            u'https://i.imgur.com/W3QbWFW.jpg',
                            u'https://i.imgur.com/nrkmWGn.jpg',
                            u'https://i.imgur.com/bo8kVkR.jpg']
    print('[get_img_urls_artical] ok!')

if __name__ == '__main__':
    test_get_img_urls_artical()

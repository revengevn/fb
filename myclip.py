import requests
from bs4 import BeautifulSoup

#V_URL = "http://myclip.vn/video/3055902/seer-anh-hung-v-tr-phn-1-tp-16-hot-hinh-hay"
V_URL = "http://myclip.vn/video/3183231"


def BR(url):
    uAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    session = requests.Session()
    session.headers.update({'User-Agent': uAgent})
    session.headers.update({'allow_redirects': 'True'})
    return session.get(url, stream=True)


def build_ts_files():
    html = BR(V_URL).content
    soup = BeautifulSoup(html, 'html.parser')
    # info-video width-common
    m3u8_url = soup.find('div', {'class': 'info-video width-common'}
                         ).find('input', {'id': 'url'}).get('value')

    # last url in list (1080->720->480)
    f = BR(m3u8_url).text.rstrip().split('\n')
    f_name = m3u8_url.split('/')[-1]

    m3u8_url = m3u8_url.replace(f_name, f[-1])

    ts = []
    for t in BR(m3u8_url).text.rstrip().split('\n'):
        if(t.find('#') != 0):
            ts.append(m3u8_url.replace(m3u8_url.split('/')[-1], t))

    return ts


def download():
    file_name = './' + V_URL.split('/')[-1] + ".mp4"
    f = open(file_name, 'wb')
    for t in build_ts_files():
        for chunk in BR(t).iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    f.close()


download()


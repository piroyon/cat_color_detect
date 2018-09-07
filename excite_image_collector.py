import os
import sys
from time import time, sleep
from urllib.request import urlopen, Request
from urllib.parse import quote
from bs4 import BeautifulSoup
import hashlib
import sha3
import urllib
import requests
from PIL import Image

MY_EMAIL_ADDR = 'a@b.c'  #your mail address

class Fetcher:
    def __init__(self, ua=''):
        self.ua = ua

    def fetch(self, url):
        req = Request(url, headers={'User-Agent': self.ua})
        try:
            with urlopen(req, timeout=3) as p:
                b_content = p.read()
                mime = p.getheader('Content-Type')
        except:
            sys.stderr.write('Error in fetching {}\n'.format(url))
            sys.stderr.write(traceback.format_exc())
            return None, None
        return b_content, mime

fetcher = Fetcher(MY_EMAIL_ADDR)

def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def split_filename(f):
    split_name = os.path.splitext(f)
    file_name =split_name[0]
    extension = split_name[-1].replace(".","")
    return file_name,extension

def fetch_and_save_img(word):
    kl = word.split('+')
    path = 'catimage/' + kl[1]
    make_dir(path)
    for j in range(5):
        h = j + 1
        for i, img_url in enumerate(img_url_list(word, h)):
            sleep(0.1)
            _,extension  = split_filename(img_url)
            if extension.lower() in ('jpg','jpeg','png'):
                encode_url = urllib.parse.unquote(img_url).encode('utf-8')
                hashed_name = hashlib.sha3_256(encode_url).hexdigest()
                result_file = os.path.join(path, hashed_name + '.' + extension.lower())
                r = requests.get(img_url)
                if r.status_code == requests.codes.ok:
                    with open(result_file, mode='wb') as f:
                        f.write(r.content)
                        print('fetched', img_url)
                        if (extension.lower() == 'png'):
                            png_im = Image.open(result_file).convert('P')
                            rgb_im = png_im.convert('RGB')
                            jpg_file = os.path.join(path, hashed_name + '.jpg')
                            rgb_im.save(jpg_file, quality=30)
                            os.remove(result_file)



def img_url_list(word, page):
    url = 'https://imagesearch.excite.co.jp/?q={}&page='.format(quote(word))
    url += str(page)
    print(url)
    byte_content, _ = fetcher.fetch(url)
    structured_page = BeautifulSoup(byte_content.decode('UTF-8'), 'html.parser')
    img_link_elems = structured_page.find_all('a', attrs={'rel': 'lightbox[result]'})
    img_urls = [e.get('href') for e in img_link_elems if e.get('href').startswith('http')]
    img_urls = list(set(img_urls))
    return img_urls

if __name__ == '__main__':
    args = sys.argv
    query = 'cat+'
    args.pop(0)
    length = len(args)
    color1 = args[0]
    for idx, color in enumerate(args):
        query = query + color
        if (idx != length-1):
            query = query + '+'
    fetch_and_save_img(query)

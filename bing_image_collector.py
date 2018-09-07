# -*- coding: utf-8 -*-
import sys
import os
import math
import urllib
import hashlib
import sha3
import requests
import time

args = sys.argv
query = 'cat '  #"cat is default query, plz input keyword color"
args.pop(0)
length = len(args)
color1 = args[0]
for idx, color in enumerate(args):
    query = query + color
    if (idx != length-1):
        query = query + ' '

def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def split_filename(f):
    split_name = os.path.splitext(f)
    file_name =split_name[0]
    extension = split_name[-1].replace(".","")
    return file_name,extension

def download_img(path,url):
    make_dir(path)
    _,extension  = split_filename(url)
    if extension.lower() in ('jpg','jpeg','png'):
        encode_url = urllib.parse.unquote(url).encode('utf-8')
        hashed_name = hashlib.sha3_256(encode_url).hexdigest()
        full_path = os.path.join(path,hashed_name + '.' + extension.lower())

        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            with open(full_path,'wb') as f:
                f.write(r.content)
                if (extension.lower() == 'png'):
                    png_im = Image.open(full_path).convert('P')
                    rgb_im = png_im.convert('RGB')
                    jpg_file = os.path.join(path, hashed_name + '.jpg')
                    rgb_im.save(jpg_file, quality=30)
                    os.remove(full_path)
            print('saved image...{}'.format(url))
        else:
            print("HttpError:{0}  at{1}".format(r.status_code,url))


if __name__ == '__main__':
    bing_api_key = '95cc4440be084158ba1767fea2bac821'  #your bing api key

    save_dir_path = './catimage/' + color1
    make_dir(save_dir_path)

    num_imgs_required = 300 # Number of images you want.
    num_imgs_per_transaction = 50 # default 30, Max 150 images
    offset_count = math.floor(num_imgs_required / num_imgs_per_transaction)

    url_list = []
    correspondence_table = {}

    headers = {
        # Request headers
        'Content-Type': 'multipart/form-data',
        'Ocp-Apim-Subscription-Key': bing_api_key
    }

    bingurl = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

    for offset in range(int(offset_count)):

        params = urllib.parse.urlencode({
            'q': query,
            'mkt': 'ja-JP',
            'imageType': 'Photo',
            'count': num_imgs_per_transaction,
            'offset': offset * num_imgs_per_transaction # increment offset by 'num_imgs_per_transaction' (for example 0, 150, 300)
        })

        try:
            response = requests.get(bingurl, headers=headers, params=params)
            data = response.json()

        except Exception as err:
            print("[Errno {0}] {1}".format(err.errno, err.strerror))

        else:
            for values in data['value']:
                img_url = values['contentUrl']
                try:
                    download_img(save_dir_path,img_url)
                except Exception as e:
                    print("failed to download image at {}".format(img_url))
                    print(e)
            time.sleep(1)

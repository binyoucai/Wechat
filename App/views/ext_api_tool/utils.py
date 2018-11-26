# -*-coding:utf-8 -*-
import requests
import json
import threading
import time
import os

from App.settings import IMAGE_DIR, FACE_DIR, WX_TOKEN, WX_SECRET_KEY, WX_APP_ID

token = WX_TOKEN
app_id = WX_APP_ID
secret = WX_SECRET_KEY


def img_download(url, name):
    if not os.path.isdir(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)
    r = requests.get(url)
    if r.status_code == 200:
        with open('{}/{}-{}.jpg'.format(IMAGE_DIR, name, time.strftime("%Y_%m_%d%H_%M_%S", time.localtime())),
                  'wb') as f:
            f.write(r.content)
        if os.path.getsize(f.name) >= 1048576:
            return 'large'
        print('namename', os.path.basename(f.name))
        return os.path.basename(f.name)
    else:
        return 'download not'


def get_access_token(appid, secret):
    '''获取access_token,100分钟刷新一次'''

    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(appid,
                                                                                                           secret)
    r = requests.get(url)
    parse_json = json.loads(r.text)
    global token
    token = parse_json['access_token']
    global timer
    timer = threading.Timer(6000, get_access_token)
    timer.start()


def img_upload(mediaType, name):
    global token

    if not os.path.isdir(FACE_DIR):
        os.mkdir(FACE_DIR)

    url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (token, mediaType)
    files = {'media': open('{}'.format(name), 'rb')}
    r = requests.post(url, files=files)
    parse_json = json.loads(r.text)
    return parse_json['media_id']


get_access_token(app_id, secret)

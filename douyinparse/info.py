# -*- coding: UTF-8 -*-
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from douyinparse.auth import login_required
from douyinparse.db import get_db
import requests, re, time
from hyper.contrib import HTTP20Adapter

bp = Blueprint('info', __name__)

@bp.route('/')
@login_required
def index():
    return redirect(url_for('info.showres'))

def geturl(text):
    pat = re.compile(r"https://v.douyin.com/(\w+)/ 复制此链接")
    path = "".join(pat.findall(text))
    url = 'https://v.douyin.com/'+ path +'/'
    return url, path

def getvid(url, path):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'cookie': '_ga=GA1.2.1944256348.1589814119; _gid=GA1.2.1033517079.1590582968',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'upgrade-insecure-requests': '1',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        ':authority': 'v.douyin.com',
        ':method': 'GET',
        ':path': '/'+path+'/',
        ':scheme': 'https',
    }
    sessions = requests.session()
    sessions.mount('https://v.douyin.com', HTTP20Adapter())
    response = sessions.get(url=url, headers=headers)
    res = str(response.headers[b'location'], encoding='utf-8')
    pat = re.compile(r"/video/(\d+)/\?region=CN")
    vid = "".join(pat.findall(res))
    return vid, res

def getcid(username, vid):
    page = 0
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Host': '47.115.206.218',
        'Referer': 'http://47.115.206.218/comment/?page='+str(page-1)+'&itemid='+vid
    }
    pat = re.compile(r"""<tr>
                        <td >(\d+)</td>
                        <td>(.+)</td>
                        <td style="font-size: 14px">(.+)</td>
                        <td>(\d+)</td>
                        <td>(.+)</td>
                        <td>(\d+)</td>
                        <td>(\d+)</td>
                        <td>(\d+)</td>
                        <td>(\d+)</td>
                        </tr>""")
    while True:
        url = 'http://47.115.206.218/comment/?page='+str(page)+'&itemid='+vid
        r = requests.get(url, headers=headers)
        res = pat.findall(r.text)
        for id, name, comment, dnum, ctime, aweme_id, cid, uid, sid in res:
            if name == username:
                return cid
        page += 1
        time.sleep(3)
        if len(res) == 0:
            break

@bp.route('/infolist', methods=('GET', 'POST'))
@login_required
def showres():
    if request.method == 'POST':
        sharetxt = request.form['sharetxt']
        error = None

        if not sharetxt:
            error = "分享链接不能为空！"
        url, path = geturl(sharetxt)
        vid, res = getvid(url, path)
        cid = getcid(g.user['username'], vid)
        if cid is None:
            error = "查询失败，请重试或更换分享链接！"
        if error is None:
            return render_template('info/list.html', url=res, video=vid, comment=cid)
        flash(error)
    return render_template('info/list.html')
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

def old_getcid(username, vid, page=0):
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

def new_getcid(username, vid, cursor=0):
    headers = {
        'X-Token': '925767B8A4BF11EA903B88E9FE880485',
        'Content-Type': 'application/json'
    }
    url = 'https://cloud.anoyi.com/api/dyapp/comment/list'
    data = {
        'device': 'os_api=22&device_type=TAS-AN00&ssmix=a&manifest_version_code=110301&dpi=254&uuid=868915849736228&app_name=aweme&version_name=11.3.0&ts=1591521668&cpu_support64=false&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code=11309900&channel=aweGW&_rticket=1591521711306&device_platform=android&iid=2981522457757277&version_code=110300&mac_address=60%3A9d%3Aa0%3A01%3A04%3A26&cdid=5a45f2e0-bad5-49e1-b25d-d2523e0aec06&openudid=ccb54e8961b6eaec&device_id=237140060934743&resolution=768*1366&os_version=5.1.1&language=zh&device_brand=HUAWEI&aid=1128&mcc_mnc=46000',
        'cookie': 'install_id=2981522457757277; ttreq=1$a25b756540eb001f9b82b638f1eef138fa0365b7; passport_csrf_token=fe6592c1db2b757f44b9ecd2e5084bbc; d_ticket=0773415f0b65cba74d9d40408c8a5d80e2a68; odin_tt=4fe90b5298753bd5747399bd521a42a7372403de14f058dadf51842db90da8b1550578039a4003e14e9e64a86082cc88961bd643ea6029d3fb4198d9399d5b2c; sid_guard=3288b322d8ff9279214c04a27e52f3a5%7C1591521379%7C5184000%7CThu%2C+06-Aug-2020+09%3A16%3A19+GMT; uid_tt=5216541b00ff7428a7e05245c51683f9; sid_tt=3288b322d8ff9279214c04a27e52f3a5; sessionid=3288b322d8ff9279214c04a27e52f3a5',
        'x-tt-token': '003288b322d8ff9279214c04a27e52f3a55689de412f9d157182fbdb28d1d24d0ea41fae3233db9cfa35b632e7679769241a',
        'aweme_id': vid,
        'cursor': cursor
    }

    r = requests.post(url, headers=headers, json=data)
    dyheaders = r.json()['data']['headers']
    dyurl = r.json()['data']['url']

    dyresponse = requests.get(dyurl, headers=dyheaders)
    comments = dyresponse.json()['comments']
    if comments is None:
        return "Done"
    result = [(
        item.get('cid', 'NA'),
        item.get('text', 'NA'),
        item.get('aweme_id', 'NA'),
        time.strftime("%Y-%m-%d/%H:%M:%S", time.localtime(item.get('create_time', 'NA'))),
        item.get('digg_count', 'NA'),
        item.get('user', 'NA').get('uid', 'NA'),
        item.get('user', 'NA').get('short_id', 'NA'),
        item.get('user', 'NA').get('nickname', 'NA')
    ) for item in comments]
    # print(result)
    for cid, text, aweme_id, create_time, digg_count, uid, short_id, nickname in result:
        if nickname == username:
            return cid
    cursor = dyresponse.json()['cursor']
    if cursor <= 140:
        return new_getcid(username, vid, cursor)
    else:
        return "Loser"

@bp.route('/infolist', methods=('GET', 'POST'))
@login_required
def showres():
    if request.method == 'POST':
        sharetxt = request.form['sharetxt']
        error = None

        if not sharetxt:
            error = "分享链接不能为空！"
        else:
            url, path = geturl(sharetxt)
            vid, res = getvid(url, path)
            if request.form['action'] == "老版查询":
                cid = old_getcid(g.user['username'], vid)
            elif request.form['action'] == "新版查询":
                cid = new_getcid(g.user['username'], vid)
            if cid is None:
                error = "查询失败，请重试或更换分享链接！"
            elif cid == "Loser":
                error = "新版查询前七页无查询结果，请重新评论、分享！"
            elif cid == "Done":
                error = "该用户未对此视频发表任何评论！"
        if error is None:
            return render_template('info/list.html', url=res, video=vid, comment=cid)
        flash(error)
    return render_template('info/list.html')
import requests, time

# headers = {
#     'X-Token': '925767B8A4BF11EA903B88E9FE880485',
#     'Content-Type': 'application/json'
# }
# url = 'https://cloud.anoyi.com/api/dyapp/comment/list'
# data = {
#     'device': 'os_api=22&device_type=TAS-AN00&ssmix=a&manifest_version_code=110201&dpi=254&uuid=868915849736228&app_name=aweme&version_name=11.2.0&ts=1591194819&cpu_support64=false&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code=11209900&channel=aweGW&_rticket=1591194815749&device_platform=android&iid=2612085197116808&version_code=110200&mac_address=60%3A9d%3Aa0%3A01%3A04%3A26&cdid=06a8ca5f-7957-4405-aaa5-44f0c9fa7f35&openudid=ccb54e8961b6eaec&device_id=237140060934743&resolution=768*1366&os_version=5.1.1&language=zh&device_brand=HUAWEI&aid=1128&mcc_mnc=46000',
#     'cookie': 'passport_csrf_token=c857cca19c41e367132c0939f82dd89f; d_ticket=093066307e7dfaa2c187bab6ba618d8ae2a68; odin_tt=e0d8155184c7c74b4a3c44787f6fa69eec0c120a2a7f6b6471e667989612098acfce8f03cb9bafbb17d981e1034ae03f54ed5bef0a3e4eb6da753024635f56f3; sid_guard=d37020fb99658868ff0a74dceaa40973%7C1591190814%7C5184000%7CSun%2C+02-Aug-2020+13%3A26%3A54+GMT; uid_tt=0943ec3de9cd43b7937009e051e18339; sid_tt=d37020fb99658868ff0a74dceaa40973; sessionid=d37020fb99658868ff0a74dceaa40973',
#     'x-tt-token': '00d37020fb99658868ff0a74dceaa409735c9f38f98eb1bf66f247d676e8eacbd5a5b1f3a0b575d6d9341a1ebd75b797fe3',
#     'aweme_id': '6826546086967086343',
#     'cursor': '20'
# }

# r = requests.post(url, headers=headers, json=data)
# dyheaders = r.json()['data']['headers']
# dyurl = r.json()['data']['url']

# dyresponse = requests.get(dyurl, headers=dyheaders)
# print(type(dyresponse.json()))
# comments = dyresponse.json()['comments']

# result = [(
#     item.get('cid', 'NA'),
#     item.get('text', 'NA'),
#     item.get('aweme_id', 'NA'),
#     time.strftime("%Y-%m-%d/%H:%M:%S", time.localtime(item.get('create_time', 'NA'))),
#     item.get('digg_count', 'NA'),
#     item.get('user', 'NA').get('uid', 'NA'),
#     item.get('user', 'NA').get('short_id', 'NA'),
#     item.get('user', 'NA').get('nickname', 'NA')
# ) for item in comments]
# print(result)
# print(dyresponse.json()['cursor'])


def getcid(username, vid, cursor=0):
    headers = {
        'X-Token': '925767B8A4BF11EA903B88E9FE880485',
        'Content-Type': 'application/json'
    }
    url = 'https://cloud.anoyi.com/api/dyapp/comment/list'
    data = {
        'device': 'os_api=22&device_type=TAS-AN00&ssmix=a&manifest_version_code=110201&dpi=254&uuid=868915849736228&app_name=aweme&version_name=11.2.0&ts=1591194819&cpu_support64=false&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code=11209900&channel=aweGW&_rticket=1591194815749&device_platform=android&iid=2612085197116808&version_code=110200&mac_address=60%3A9d%3Aa0%3A01%3A04%3A26&cdid=06a8ca5f-7957-4405-aaa5-44f0c9fa7f35&openudid=ccb54e8961b6eaec&device_id=237140060934743&resolution=768*1366&os_version=5.1.1&language=zh&device_brand=HUAWEI&aid=1128&mcc_mnc=46000',
        'cookie': 'passport_csrf_token=c857cca19c41e367132c0939f82dd89f; d_ticket=093066307e7dfaa2c187bab6ba618d8ae2a68; odin_tt=e0d8155184c7c74b4a3c44787f6fa69eec0c120a2a7f6b6471e667989612098acfce8f03cb9bafbb17d981e1034ae03f54ed5bef0a3e4eb6da753024635f56f3; sid_guard=d37020fb99658868ff0a74dceaa40973%7C1591190814%7C5184000%7CSun%2C+02-Aug-2020+13%3A26%3A54+GMT; uid_tt=0943ec3de9cd43b7937009e051e18339; sid_tt=d37020fb99658868ff0a74dceaa40973; sessionid=d37020fb99658868ff0a74dceaa40973',
        'x-tt-token': '00d37020fb99658868ff0a74dceaa409735c9f38f98eb1bf66f247d676e8eacbd5a5b1f3a0b575d6d9341a1ebd75b797fe3',
        'aweme_id': vid,
        'cursor': cursor
    }

    r = requests.post(url, headers=headers, json=data)
    dyheaders = r.json()['data']['headers']
    dyurl = r.json()['data']['url']

    dyresponse = requests.get(dyurl, headers=dyheaders)
    comments = dyresponse.json()['comments']

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
    print(result)
    for cid, text, aweme_id, create_time, digg_count, uid, short_id, nickname in result:
        if nickname == username:
            return cid
    cursor = dyresponse.json()['cursor']
    print(cursor)
    return getcid(username, vid, cursor)


print(getcid("叫我薛姐姐吖🥰", "6834031815276137741"))
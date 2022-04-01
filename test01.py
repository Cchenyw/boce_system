import datetime
import os
import time
import re

import requests
import pandas as pd


def date_judge(mission_name):
    today_str = str(time.localtime().tm_mon) + '.' + str(time.localtime().tm_mday)
    name_sp = re.split('-', mission_name)
    old_date = datetime.datetime.strptime(name_sp[1], '%m.%d')
    new_date = datetime.datetime.strptime(today_str, '%m.%d')
    print('old_date:%s,new_date:%s' % (name_sp[1], today_str))
    print(f'old_date >= new_date ? {old_date >= new_date}')
    if old_date < new_date:
        new_name = name_sp[0] + '-' + today_str + '-' + name_sp[2]
        print('update')
        return new_name
    else:
        print('remain')
        return mission_name


# 获取最新的文件
def get_old_file(file_path):
    file_list = os.listdir(file_path)
    file_list.sort(key=lambda f: os.path.getmtime(file_path + os.sep + f))
    print('last fix:' + file_list[-1])
    return file_path + '/' + file_list[-1]


def update_mission_name(file_path):
    # 这里要加上文件名称，实现每日新增一份任务清单，增量保存
    df_missions = pd.read_excel(get_old_file(f'{file_path}/mission-settings'), index_col=False)
    df_missions['任务名称'] = df_missions['任务名称'].apply(lambda x: date_judge(x))
    print(df_missions)
    file_name = f'mission-setting-{time.strftime("%Y%m%d")}.xlsx'
    df_missions.to_excel(f'{file_path}/mission-settings/{file_name}', index=False)
    return file_name


def upload_mission(file_path, cookies):
    excel_file = open(get_old_file(f'{file_path}/mission-settings'), 'rb')
    return requests.post('http://39.97.99.199/api/task/upload', headers={'Cookie': cookies}, files={'file': excel_file})


# 通过判断呼叫中任务为空来断定是否所有任务完成
def is_all_complete(cookies):
    res = requests.get('http://39.97.99.199/api/tasks/joined?begin=0&end=10', headers={
        'Cookie': cookies
    })
    if res.status_code == 200:
        if res.json()['total'] == 0:
            return True
        else:
            return False
    else:
        print(f'error:\n{res.json()}')
        return False


# count未完成任务数
def remain_missions(cookies):
    res = requests.get('http://39.97.99.199/api/tasks/joined?begin=0&end=10', headers={
        'Cookie': cookies
    })
    return res.json()['total']


def start_mission():
    pass


def download_call_detail(file_path, cookies):
    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday
    begin = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
    end = time.mktime((year, month, day, 9, 9, 9, 9, 9, 9))
    res = requests.get(
        'http://39.97.99.199/api/call-detail/batch/excel/download?page=1&page_size=10&call_begin=1648569600000&call_end=1648655999999&sort_field=start&sort_dire=desc',
        headers={
            'Cookie': cookies
        }, params={
            'page': 1,
            'page_size': 250,
            'call_begin': begin,
            'call_end': end,
            'sort_field': 'start',
            'sort_dire': 'desc'
        }, stream=True)
    if res.status_code == 200:
        filename = f'call-detail-{time.strftime("%Y%m%d")}.xlsx'
        with open(f'{file_path}/call-details/{filename}', 'wb') as f:
            for chunk in res.iter_content(1024):
                f.write(chunk)


def analysis_result(file_path):
    df = pd.read_excel(get_old_file(f'{file_path}/call-details'))
    UC_passed_ratio = calc_pass_ratio(df, 'v2_UC', '通过')
    taobao_passed_ratio = calc_pass_ratio(df, 'v2淘宝天猫', '通过')
    xianyu_passed_ratio = calc_pass_ratio(df, 'v2_闲鱼', '通过')
    gaode_passed_ratio = calc_pass_ratio(df, 'v2_高德', '通过')
    dingding_passed_ratio = calc_pass_ratio(df, 'v2_钉钉', '通过')
    result = {
        'UC_passed_ratio': UC_passed_ratio,
        'taobao_passed_ratio': taobao_passed_ratio,
        'xianyu_passed_ratio': xianyu_passed_ratio,
        'gaode_passed_ratio': gaode_passed_ratio,
        'dingding_passed_ratio': dingding_passed_ratio
    }
    print(result)
    df['UC通过率'] = UC_passed_ratio
    df['淘宝通过率'] = taobao_passed_ratio
    df['闲鱼通过率'] = xianyu_passed_ratio
    df['高德通过率'] = gaode_passed_ratio
    df['钉钉通过率'] = dingding_passed_ratio
    file_name = f'result-{time.strftime("%Y%m%d")}.xlsx'
    df.to_excel(f'{file_path}/results/{file_name}', index=False)


def calc_pass_ratio(df, company_name, test_result):
    passed_call = df[(df['对应企业'] == f'{company_name}') & (df['测试结果'] == f'{test_result}')]
    all_call = df[(df['对应企业'] == f'{company_name}')]
    return len(passed_call) / len(all_call)


if __name__ == "__main__":
    windows_path = 'C:/Users/TUNGEE/Desktop/项目/中国通信院-拨测系统'
    mac_path = '/Users/chenyw/Downloads'
    cookie = 'remember_token=6242bdca8b98ed524818a927|a9a2afe0ccdd1da24e54ffef3c020770ffda34fa8e6f228b25c00b80b9cca6805cb1a85be609ef2deecfead584118ab9cddd040da16a269c646fd7f10139ef10; sessionId=.eJxFjstqwzAQRf9Fa1NGsh6jbOsSCnW8cQjtxow0oyYlcSBKW0Lpv9dk0-U9nAP3R80iPFX6kul6njipVaFjlUZN5SJ1_z8PrFYKiKm1GiwV9jbmiAEjQio2tK32YqMOwRaK2iEvhCQCJ_LaeYckpYQAPptFF0HMkh1pT2KCLt6AJusjGAAX2XvXao2mJYqMLbmUPRvVqIuc5JTkMlXJ55mrWqG3AA_QqM-64PtPb6xJnAlTRGFnLGqkaMLS17vwtu7NsNva1_H92o98GB4BhnF_eNk9677L1826d5vu6TZ021v_sXVLmPc0z3Jc4m9J6vcP8EVcIA.YkO2_g.jkLRo5bx2uYuO40EiZcfm17wBQw'
    update_mission_name(windows_path)
    r = upload_mission(windows_path, cookie)
    print(r.json())
    print('is all complete:' + str(is_all_complete(cookie)))
    time.sleep(120)
    while not (is_all_complete(cookie)):
        print(f'任务未完成,完成进度:{((250 - remain_missions(cookie)) / 250) * 100}%,剩余:{remain_missions(cookie)}个')
        time.sleep(360)
    download_call_detail(windows_path, cookie)
    time.sleep(60)
    analysis_result(windows_path)

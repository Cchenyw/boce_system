import datetime
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


def update_mission_name(file_path):
    # 这里要加上文件名称，实现每日新增一份任务清单，增量保存
    df_missions = pd.read_excel(f'{file_path}/old_file_name', index_col=False)
    df_missions['任务名称'] = df_missions['任务名称'].apply(lambda x: date_judge(x))
    print(df_missions)
    df_missions.to_excel(f'{file_path}/new_file_name', index=False)
    return f'{file_path}/new_file_name'


def upload_mission(excel_file, cookies):
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


def start_mission():
    pass


if __name__ == "__main__":
    windows_path = 'C:/Users/TUNGEE/Downloads/phone-number-template.xlsx'
    mac_path = '/Users/chenyw/Downloads/phone-number-template(1).xlsx'
    cookie = 'remember_token=6242bdca8b98ed524818a927|a9a2afe0ccdd1da24e54ffef3c020770ffda34fa8e6f228b25c00b80b9cca6805cb1a85be609ef2deecfead584118ab9cddd040da16a269c646fd7f10139ef10; sessionId=.eJxFzk9rAjEQBfDvkrOUyZ-dJN4KailUhVYo7GVJZiao3V3B2Eot_e5dvPT4Hu8H70eNItzV9CXd5dRxVvOS-ioz1ZWz1P1_PLCaK9LBlOi8drokazW4YrSGhtByDNZg8mC4UEYPlorh3MTEPgpqLZiFxVCK2Tu2JmpvEUjAJmwEUYxmJABMTOQDoQ-sLUCi5BvPbL1GNVNnGWTIcu6q0GnkquYBHcADzNRnner7TzTOZKYUcgzCjXFBhxSNn3y9DzbHZ7PZLb_Xw_Kyvj3e2jeAzbA6vOz6vj1-XNodme3TamjfXw_bBV0nSPs0jtJP-CpZ_f4BfzpeAw.YkMxNg.SiHf752V_wpJ355-fjNMMwqrpvA'
    # update_mission_name(mac_path)
    # ex_file = open(mac_path, 'rb')
    # r = upload_mission(ex_file, cookie)
    # print(r.json())
    print(is_all_complete(cookie))

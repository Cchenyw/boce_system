import datetime
import time
import re

import requests
import pandas as pd


def date_judge(mission_name):
    today_str = str(time.localtime().tm_mon) + '.' + str(time.localtime().tm_mday)
    name_sp = re.split('-', mission_name)
    print(today_str)
    print(name_sp)
    old_date = datetime.datetime.strptime(name_sp[1], '%m.%d')
    print(old_date)
    new_date = datetime.datetime.strptime(today_str, '%m.%d')
    print(new_date)
    print(f'{old_date >= new_date}')
    if old_date < new_date:
        new_name = name_sp[0] + '-' + today_str + '-' + name_sp[2]
        return new_name
    else:
        return mission_name


def update_mission_name():
    df_missions = pd.read_excel('C:/Users/TUNGEE/Downloads/phone-number-template.xlsx', index_col=False)
    print(df_missions.loc[0:5, ['拨打号码']])
    print(df_missions.index)
    # print(date_judge(df_missions[['任务名称'][0]]))
    name_date = ''
    df_missions['任务名称'] = df_missions['任务名称'].apply(lambda x: date_judge(x))
    print(df_missions)


def upload_mission(excel_file):
    return requests.post('http://39.97.99.199/api/task/upload', headers={
        'Cookie': 'remember_token=6242bdca8b98ed524818a927|a9a2afe0ccdd1da24e54ffef3c020770ffda34fa8e6f228b25c00b80b9cca6805cb1a85be609ef2deecfead584118ab9cddd040da16a269c646fd7f10139ef10; sessionId=.eJxFjstOwzAQRf_F6wqNHT_G3bXqkoRNAJVNNPaMaaBNpbpQKOLfibpheY_Oke6PmkR4qPQpw_k4cFLLQvsqCzWUk9Td_xxZLRUQU2M1WCrsbcwRA0aEVGxoGu3FRh2CLRS1Q54JSQRO5LXzDklKCQF8NrMugpglO9KexARdvAFN1kcwAC6y967RGk1DFBkbcil7NmqhTnKQQ5LTUCUfJ65qid4C3MFCfdQZ3356Y03iTJgiCjtjUSNFE-a-3oR2k227eRq7t_dz229tNwJ0m_Xuvn_92j4_nrvrCrrr9vuhX11e-hXMYd7RNMl-ji-S1O8fCMNcvA.YkLBQQ.FT49LR-SPM3iHINEMiJScYF2TCA'},
                         files={'file': excel_file})


def start_mission():
    pass


if __name__ == "__main__":
    ex_file = open('C:/Users/TUNGEE/Downloads/phone-number-template.xlsx', 'rb')
    r = upload_mission(ex_file)
    print(r.json())

    update_mission_name()

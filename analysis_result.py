import time

import pandas as pd
from test01 import get_old_file


# def analysis_result(file_path):
#     df = pd.read_excel(get_old_file(f'{file_path}/call-details'))
#     UC_passed_ratio = calc_pass_ratio(df, 'v2_UC', '通过')
#     taobao_passed_ratio = calc_pass_ratio(df, 'v2淘宝天猫', '通过')
#     xianyu_passed_ratio = calc_pass_ratio(df, 'v2_闲鱼', '通过')
#     gaode_passed_ratio = calc_pass_ratio(df, 'v2_高德', '通过')
#     dingding_passed_ratio = calc_pass_ratio(df, 'v2_钉钉', '通过')
#     result = {
#         'UC_passed_ratio': UC_passed_ratio,
#         'taobao_passed_ratio': taobao_passed_ratio,
#         'xianyu_passed_ratio': xianyu_passed_ratio,
#         'gaode_passed_ratio': gaode_passed_ratio,
#         'dingding_passed_ratio': dingding_passed_ratio
#     }
#     print(result)
#     df['UC通过率'] = UC_passed_ratio
#     df['淘宝通过率'] = taobao_passed_ratio
#     df['闲鱼通过率'] = xianyu_passed_ratio
#     df['高德通过率'] = gaode_passed_ratio
#     df['钉钉通过率'] = dingding_passed_ratio
#     file_name = f'result-{time.strftime("%Y%m%d")}.xlsx'
#     df.to_excel(f'{file_path}/results/{file_name}', index=False)
#
#
# def calc_pass_ratio(df, company_name, test_result):
#     passed_call = df[(df['对应企业'] == f'{company_name}') & (df['测试结果'] == f'{test_result}')]
#     all_call = df[(df['对应企业'] == f'{company_name}')]
#     return len(passed_call) / len(all_call)


if __name__ == "__main__":
    excel_path = 'C:/Users/TUNGEE/Desktop/项目/中国通信院-拨测系统'
    analysis_result(excel_path)

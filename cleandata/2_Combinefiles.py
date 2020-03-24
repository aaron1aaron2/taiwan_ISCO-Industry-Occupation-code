import pandas as pd
import  re
import os
os.chdir(r'G:/共用雲端硬碟/資料科學小組/任務3_行職業文字轉ISCO_08代碼/cleandata') # 設定工作路徑

from src.utils import get_allfile

labelCSV_ls = get_allfile(path = '..\\raw_data\\社會變遷資料\\' , pat =r'限制.*label.csv', path_type='related')
labelCSV_ls = [(path.split('\\')[-1],path) for path in labelCSV_ls]


result = pd.DataFrame()
for name,path in labelCSV_ls:
    print(name)
    df_tmp = pd.read_csv(path)
    df_tmp['file_name'] = name
    df_tmp['file_path'] = path
    result = pd.concat([result,df_tmp])

result['file_year'] = result.file_name.str.extract(r'(\d*q?\d?\w?.label)')
result['file_year'] = result.file_year.str[:4]

# == 檢查資料 ============================================================================================================
# pd.set_option('display.max_columns', 30)
# pd.set_option('display.width', 10)
# print(result)
# print(result.columns)
# print(result.file_year.unique()) # len: 29
# print(result.file_name.unique()) # len: 60

# 造理來講 29 個年份，每年有兩份問卷(q1、q2)，所以有 58 個限制檔案，
# 其他兩個，一個是在 2001 有多一份問卷(q3)，另一個則是網路組的特別資料 '第七期/2017網絡組限制資料'
# 所以最後總共是 60 份資料。


# print(result.col_lab.unique()) # len: 19983/22198
# a = result.col_lab.value_counts() # >10 len: 22
# a[a>2].to_csv('output/2_col_lab_count.csv')

# print(result.col_name.unique()) # len: 11347/22198
# a = result.col_name.value_counts() # >10 len: 228

# print(result.val_lab.unique()) # len: 4870/20209

# 可以看到中文的 col_lab 幾乎都對不上，只有 22 題目在不同問卷出現 10 次以上
# ========================================================================================================================

# === 獲取資料中的年分資訊 =============================================================================================
def get_yearsDF(datafile):
    '''
    測試，有多少資料有多個年分的狀況
    retrun:: datapath ; years DF
    '''
    years = []
    for path in datafile:
        df = pd.read_csv(path)
        year = df.year.unique()
        year = [str(int(i)) for i in year]
        year = ','.join(year)
        years.append(year)
    years = list(years)

    years_DF = pd.DataFrame({'file_path':datafile,'data_year':years})

    return years_DF

file_ls = result.file_path.str.replace('.label','').unique()
years_DF = get_yearsDF(file_ls)
years_DF['file_path'] = years_DF.file_path.str.replace('.csv','.label.csv')
result = pd.merge(result,years_DF,how='left')


result.to_csv('output/2_all_label_file.csv', index=False)

check = df[['file_path','file_year','data_year']].drop_duplicates()
with pd.ExcelWriter('output/2_check_result_years.xlsx', mode='a+') as writer:
    check.to_excel(writer, index=False, sheet_name='check_year')
# -*- coding=utf-8 -*-
import pandas as pd
import numpy as np
import pygsheets
import re
import os
os.chdir('G:/共用雲端硬碟/資料科學小組/任務3_行職業文字轉ISCO_08代碼/cleandata')

from src.utils import check_pat_extract

df = pd.read_csv('output/2_all_label_file.csv')


# === 清理 col_lab 欄位的題號 ================================================================================================
df['col_lab'] = df['col_lab'].str.strip()
patterns = [r'(^\w+\s|^\w+\.)',r'(^[a-zA-Z_\d]+[a-zA-Z\.\d])',r'(^[a-zA-Z_\.\d]*[a-zA-Z\.\d])']
result = check_pat_extract(df, target='col_lab', pat=patterns, output_file=True, label='篩出題目')
df['col_lab'] = result.apply(lambda x: x['col_lab'].replace(str(x['result_2']),'').strip(),axis=1)

df.to_csv('output/3_all_label_clear_col_lab.csv', index=False)


# === 比對 標籤關鍵字 裡的 pattern ====================================================================================================
df = pd.read_csv('output/3_all_label_clear_col_lab.csv')
df_label = pd.read_excel('data/標籤關鍵字.xlsx', sheet_name='類別') 
df.val_lab.fillna(' ',inplace=True)
# df_label.fillna(0,inplace=True)

col_lab_ls = df_label[df_label.target == 'col_lab'][['pat_lab', 'pattern']].values
col_lab_dt = {lab:'(%s)'%pat for lab,pat in col_lab_ls}
val_lab_ls = df_label[df_label.target == 'val_lab'][['pat_lab', 'pattern']].values
val_lab_dt = {lab:'(%s)'%pat for lab,pat in val_lab_ls}
col_name_ls = df_label[df_label.target == 'col_name'][['pat_lab', 'pattern']].values
col_name_dt = {lab:'(%s)'%pat for lab,pat in col_name_ls}

match_col_lab = check_pat_extract(df, target='col_lab', pat=list(col_lab_dt.values()), output_file=True, label='col_lab_all',
        col_name=list(col_lab_dt.keys()))
match_val_lab = check_pat_extract(df, target='val_lab', pat=list(val_lab_dt.values()), output_file=True, label='val_lab_all',
        col_name=list(val_lab_dt.keys()))
match_col_name = check_pat_extract(df, target='col_name', pat=list(col_name_dt.values()), output_file=True, label='col_name_all',
        col_name=list(col_name_dt.keys()))

tmp = df.merge(match_col_lab, how='left')
tmp = tmp.merge(match_val_lab, how='left')
tmp = tmp.merge(match_col_name, how='left')


# === 依造各主題要求配對標籤 ===================================================================================================
df_lab_edge_ls = df_label.melt(id_vars=['pat_lab', 'pattern', 'relationship', 'target'], value_vars=['match_1', 'match_2',
       'match_3', 'match_4', 'match_5', 'match_6'])
df_lab_edge_ls = df_lab_edge_ls[~df_lab_edge_ls['value'].isnull()]
df_lab_edge_ls.sort_values('value', inplace=True)
df_lab_edge_ls.to_excel('output/_temp_3_label_edge_ls.xlsx', index=False)

group_ls = df_lab_edge_ls['value'].unique()


all_pos_ls,all_neg_ls=[],[]
for group in group_ls:
    pos_ls = df_lab_edge_ls[(df_lab_edge_ls['value']==group) & (df_lab_edge_ls['relationship']==1)].pat_lab.to_list()
    neg_ls = df_lab_edge_ls[(df_lab_edge_ls['value']==group) & (df_lab_edge_ls['relationship']==-1)].pat_lab.to_list()
    all_pos_ls.append(pos_ls)
    all_neg_ls.append(neg_ls)
    if len(neg_ls) != 0:
        tmp.loc[(~tmp[pos_ls].isnull().any(axis=1))&(tmp[neg_ls].isnull().all(axis=1)),'match_result'] = group
    else:
        tmp.loc[(~tmp[pos_ls].isnull().any(axis=1)),'match_result'] = group
tmp.to_csv('output/3_all_label_match_result.csv', index=False)

# === 檢查結果 ========================================================================
# cols = ['match_result','col_name','col_lab','val_lab','file_name','file_year',
#        'data_year', 'file_path']
# count_ls,file_year_ls,col_lab_ls,val_lab_ls =[],[],[],[]
# for result in group_ls:
#     tmp_df = tmp[cols][tmp[cols].match_result==result]
#     count_ls.append(len(tmp_df))
#     file_year_ls.append(tmp_df.file_year.sort_values().unique())
#     col_lab_ls.append(tmp_df.col_lab.unique())
#     val_lab_ls.append(tmp_df.val_lab.unique())

# check = pd.DataFrame({'match_result': group_ls, 'count': count_ls, 'col_lab' :col_lab_ls, 'val_lab': val_lab_ls, 
#             'file_year': file_year_ls, 'pos_ls': all_pos_ls, 'neg_ls': all_neg_ls})


# with pd.ExcelWriter('output/3_check_all_label_match_result.xlsx', mode='a+') as writer:
#     tmp[cols].to_excel(writer, index=False, sheet_name='result_each')
#     tmp.to_excel(writer, index=False, sheet_name='result_each_all_pattern')
#     check.to_excel(writer, index=False, sheet_name='result_lab')

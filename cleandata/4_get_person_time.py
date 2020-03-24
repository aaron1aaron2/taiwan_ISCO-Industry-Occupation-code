import  pandas as pd
import os
os.chdir('G:/共用雲端硬碟/資料科學小組/任務3_行職業文字轉ISCO_08代碼/cleandata')

from src.utils import check_pat_extract


# === 身分抽取 ============================================================================================================
cols = ['match_result', 'col_name', 'col_lab', 'val_lab', 'file_name', 'file_path', 'file_year', 'data_year']
df = pd.read_csv('output/3_all_label_match_result.csv', usecols=cols)
df_label = pd.read_excel('data/標籤關鍵字.xlsx', sheet_name='身分') 

col_lab_ls = df_label[['pat_lab', 'pat']].values
col_lab_dt = {lab:'(%s)'%pat for lab,pat in col_lab_ls}

match_col_lab = check_pat_extract(df, target='col_lab', pat=list(col_lab_dt.values()), output_file=True, label='person_match',
        col_name=list(col_lab_dt.keys()))

df = df.merge(match_col_lab, how='left')

df_lab_edge_ls = df_label.melt(id_vars=['pat_lab', 'pat', 'relationship'], value_vars=['match_1'])
df_lab_edge_ls = df_lab_edge_ls[~df_lab_edge_ls['value'].isnull()]
df_lab_edge_ls.sort_values('value', inplace=True)

group_ls = df_lab_edge_ls['value'].unique()


all_pos_ls,all_neg_ls=[],[]
for group in group_ls:
    pos_ls = df_lab_edge_ls[(df_lab_edge_ls['value']==group) & (df_lab_edge_ls['relationship']==1)].pat_lab.to_list()
    neg_ls = df_lab_edge_ls[(df_lab_edge_ls['value']==group) & (df_lab_edge_ls['relationship']==-1)].pat_lab.to_list()
    all_pos_ls.append(pos_ls)
    all_neg_ls.append(neg_ls)
    if len(neg_ls) != 0:
        df.loc[(~df[pos_ls].isnull().any(axis=1))&(df[neg_ls].isnull().all(axis=1)),'match_person'] = group
    else:
        df.loc[(~df[pos_ls].isnull().any(axis=1)),'match_person'] = group

df.to_csv('output/4_all_label_match_person.csv', index=False)

# === 檢查結果 ============================================================================================================
# cols = ['match_person','col_name','col_lab','val_lab','file_name','file_year',
#        'data_year', 'file_path']
# count_ls,file_year_ls,col_lab_ls,val_lab_ls =[],[],[],[]
# for result in group_ls:
#     tmp_df = df[cols][df[cols].match_person==result]
#     count_ls.append(len(tmp_df))
#     file_year_ls.append(tmp_df.file_year.sort_values().unique())
#     col_lab_ls.append(tmp_df.col_lab.unique())
#     val_lab_ls.append(tmp_df.val_lab.unique())

# check = pd.DataFrame({'match_person': group_ls, 'count': count_ls, 'col_lab' :col_lab_ls, 'val_lab': val_lab_ls, 
#             'file_year': file_year_ls, 'pos_ls': all_pos_ls, 'neg_ls': all_neg_ls})


# with pd.ExcelWriter('output/4_check_all_label_match_person.xlsx', mode='a+') as writer:
#     df[cols].to_excel(writer, index=False, sheet_name='result_each')
#     df.to_excel(writer, index=False, sheet_name='result_each_all_pattern')
#     check.to_excel(writer, index=False, sheet_name='result_lab')


# === 時間抽取 ============================================================================================================
df_label = pd.read_excel('data/標籤關鍵字.xlsx', sheet_name='時間') 

col_lab_ls = df_label[['pat_lab', 'pat']].values
col_lab_dt = {lab:'(%s)'%pat for lab,pat in col_lab_ls}

match_col_lab = check_pat_extract(df, target='col_lab', pat=list(col_lab_dt.values()), output_file=True, label='person_match',
        col_name=list(col_lab_dt.keys()))

df = df.merge(match_col_lab, how='left')

df_lab_edge_ls = df_label.melt(id_vars=['pat_lab', 'pat', 'relationship'], value_vars=['match_1'])
df_lab_edge_ls = df_lab_edge_ls[~df_lab_edge_ls['value'].isnull()]
df_lab_edge_ls.sort_values('value', inplace=True)

group_ls = df_lab_edge_ls['value'].unique()


all_pos_ls,all_neg_ls=[],[]
for group in group_ls:
    pos_ls = df_lab_edge_ls[(df_lab_edge_ls['value']==group) & (df_lab_edge_ls['relationship']==1)].pat_lab.to_list()
    neg_ls = df_lab_edge_ls[(df_lab_edge_ls['value']==group) & (df_lab_edge_ls['relationship']==-1)].pat_lab.to_list()
    all_pos_ls.append(pos_ls)
    all_neg_ls.append(neg_ls)
    if len(neg_ls) != 0:
        df.loc[(~df[pos_ls].isnull().any(axis=1))&(df[neg_ls].isnull().all(axis=1)),'match_time'] = group
    else:
        df.loc[(~df[pos_ls].isnull().any(axis=1)),'match_time'] = group


df.to_csv('output/4_all_label_match_time.csv', index=False)

cols = ['match_result','match_person','match_time','col_name','col_lab','val_lab','file_name','file_year',
       'data_year', 'file_path']

df[cols].to_csv('output/4_all_label_final_result.csv', index=False)

# === 檢查結果 =============================================================================================================
# cols = ['match_time','col_name','col_lab','val_lab','file_name','file_year',
#        'data_year', 'file_path']
# count_ls,file_year_ls,col_lab_ls,val_lab_ls =[],[],[],[]
# for result in group_ls:
#     tmp_df = df[cols][df[cols].match_time==result]
#     count_ls.append(len(tmp_df))
#     file_year_ls.append(tmp_df.file_year.sort_values().unique())
#     col_lab_ls.append(tmp_df.col_lab.unique())
#     val_lab_ls.append(tmp_df.val_lab.unique())

# check = pd.DataFrame({'match_time': group_ls, 'count': count_ls, 'col_lab' :col_lab_ls, 'val_lab': val_lab_ls, 
#             'file_year': file_year_ls, 'pos_ls': all_pos_ls, 'neg_ls': all_neg_ls})


# with pd.ExcelWriter('output/4_check_all_label_match_time.xlsx', mode='a+') as writer:
#     df[cols].to_excel(writer, index=False, sheet_name='result_each')
#     df.to_excel(writer, index=False, sheet_name='result_each_all_pattern')
#     check.to_excel(writer, index=False, sheet_name='result_lab')


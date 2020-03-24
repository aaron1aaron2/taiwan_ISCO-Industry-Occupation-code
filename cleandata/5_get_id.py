import  pandas as pd
import os
os.chdir('G:/共用雲端硬碟/資料科學小組/任務3_行職業文字轉ISCO_08代碼/cleandata')

df = pd.read_csv('output/4_all_label_final_result.csv')

match_id = df[~df[['match_person', 'match_time']].isnull().any(axis=1)].index

gb = df.loc[match_id,:].groupby(['file_name', 'match_person', 'match_time'])

for idx,gp in enumerate(gb.groups):
    df.loc[gb.groups[gp],'person_id'] = idx

df.to_csv('output/5_all_id_result.csv', index=False)

# === 檢查結果用 ========================================================================================================
# tmp = df[df.match_result.isin(['ISCO88','ISCO08'])]

# person_ls = df.match_person.unique()

# count_ls,file_year_ls,col_lab_ls,val_lab_ls,person_id_ls,match_time_ls =[],[],[],[],[],[]
# for result in person_ls:
#     tmp_df = tmp[tmp.match_person==result]
#     count_ls.append(len(tmp_df))
#     file_year_ls.append(tmp_df.file_year.sort_values().unique())
#     col_lab_ls.append(tmp_df.col_lab.unique())
#     val_lab_ls.append(tmp_df.val_lab.unique())
#     person_id_ls.append(tmp_df.person_id.unique())
#     match_time_ls.append(tmp_df.match_time.unique())

# check = pd.DataFrame({'match_time': person_ls, 'count': count_ls, 'col_lab' :col_lab_ls, 'val_lab': val_lab_ls, 
#             'file_year': file_year_ls, 'person_id_ls': person_id_ls, 'match_time_ls': match_time_ls})

# with pd.ExcelWriter('output/5_check_person.xlsx', mode='a+') as writer:
#     df.to_excel(writer, index=False, sheet_name='all_result')
#     check.to_excel(writer, index=False, sheet_name='check_person')
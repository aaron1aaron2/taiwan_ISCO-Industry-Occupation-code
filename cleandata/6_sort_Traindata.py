import pandas as pd
import os
os.chdir(r'G:/共用雲端硬碟/資料科學小組/任務3_行職業文字轉ISCO_08代碼/cleandata') # 設定工作路徑

from IPython import embed

def select_train_data(df_input:pd.DataFrame, target:str, condition:dict=None, export_data=False, file_lab=None):
    '''將資料依造輸入的條件和目標變數，去抓取對應的資料。目標變數是必要的，因為他是我們訓練主要的參數。'''
    df = df_input.copy()

    if condition!=None:
        condition['match_result'].append(target)

        for col_name in condition:
            if 'mark' in df.columns:
                df.loc[(df[col_name].isin(condition[col_name])) & (df['mark']==True),'mark'] = True
            else:
                df.loc[df[col_name].isin(condition[col_name]),'mark'] = True

        df.loc[df['mark'].isnull(),'mark'] = False
        df = df_input[df['mark']]

    target_idx_ls = df.loc[df.match_result==target,'person_id'].unique()
    df = df[df.person_id.isin(target_idx_ls)]
    df.reset_index(drop=True, inplace=True)
    if file_lab:
        path = 'output/6_train_{}.csv'.format(file_lab)
    else:
        path = 'output/6_train_{}.csv'.format(target)
    if export_data:
        export_train_data(df, filepath=path, target=target)

    return df


def select_columns(df:pd.DataFrame):
    '''把重複的欄位篩掉，取空值少的'''
    tmp = df.copy()
    count_df = tmp.columns.value_counts()
    count_dt = count_df[count_df>1].to_dict()
    
    for key,num in count_dt.items():
        df.drop(key, axis=1, inplace=True)
        select_result = [tmp[~tmp[key].iloc[:,col_idx].isnull()].shape[0] for col_idx in range(num)]
        df.loc[:,key] = tmp[key].iloc[:,select_result.index(max(select_result))] 

    return df   

def export_train_data(df:pd.DataFrame, filepath:str='../DATA/train.csv', target:str=None):
    '''將資料匯出'''
    lab_type = pd.read_excel('data/標籤關鍵字.xlsx',sheet_name='類別標籤')
    basis_ls = lab_type.loc[lab_type.use_type=='basis','備註'].to_list()
    df['data_path'] = df.file_path.str.replace('.label','')

    file_ls = df.data_path.unique()
    df_all_result = pd.DataFrame()

    for file in file_ls:
        print('\n','>> file:',file)
        print('='*120)
        df_lab = df.loc[df.data_path==file,:].copy()
        df_lab = df_lab[~df_lab.match_result.isnull()]

        pid_dt = {pid:df_lab.loc[df_lab.person_id==pid,'col_name'].to_list() for pid in df_lab.person_id.unique()}
        pid_dt = {pid:(cols if 'id' in cols else basis_ls+cols) for pid,cols in pid_dt.items()}
        col_dt = df_lab[['col_name','match_result']].set_index('col_name').to_dict()

        df_file = pd.read_csv(file, usecols=basis_ls+df_lab.col_name.to_list())
        df_result = pd.DataFrame()
        for pid,cols in pid_dt.items():
            tmp = df_file[cols].copy()
            tmp.loc[:,'pid'] = pid
            tmp.rename(columns=col_dt['match_result'], inplace=True)
            print('  ',tmp.columns)

            if (tmp.columns.value_counts()>1).any():
                tmp = select_columns(tmp)

            tmp.loc[:,'file'] = file
            tmp = tmp[~tmp[target].isnull()]
            df_result = df_result.append(tmp, sort=True)

        df_all_result = df_all_result.append(df_result)
    
    df_all_result.to_csv(filepath, index=False)
    df_all_result


if __name__ == "__main__":
    df = pd.read_csv('output/5_all_id_result.csv')
    test = {'match_result': ['職位','行業碼','職業碼','ISCO08']}
    #result = select_train_data(df, target='ISCO88', condition=test, export_data=True)
    result = select_train_data(df, target='ISCO88', export_data=True, file_lab='all_ISCO88')
    result2 = select_train_data(df, target='ISCO08', export_data=True, file_lab='all_ISCO08')
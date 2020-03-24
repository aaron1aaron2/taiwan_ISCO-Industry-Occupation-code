import os
import re
import pygsheets
import pandas as pd

def get_allfile(path:str, pat:str, path_type:str):
    '''
    根據特定pattern找出所有子資料夾內的檔案
    '''
    if path_type not in ['absolute', 'related']:
        path_type = 'related'
    print('{} path mode'.format(path_type))
    
    inpath = os.getcwd() +'\\' + path

    pattern = re.compile(pat)
    
    res_files = []
    for dirpath, subdirs, files in os.walk(inpath):
        for x in files:
            # print(x)
            if path_type == 'absolute':
                finalPath = os.path.join(dirpath, x)
            if path_type == 'related':
                relpath = os.path.relpath(dirpath ,inpath)
                finalPath = os.path.join(relpath, x)
                finalPath = os.path.join(path,finalPath)
            if pattern.search(finalPath): 
                res_files.append(finalPath)
    return res_files

def check_pat_extract(df:pd.DataFrame, target:str, pat:list, output_file:bool=False, label:str=None, col_name:list=None):
    """

    extension function of `pandas.Series.str.extract()`,you can match `multi-pat(regular expression)` in one time to `target` of dataframe,then output 
    the file and check the result. 

    happy XD!!
    
    Parameters
    ----------
    df : pandas.DataFrame
    target: str
        target columns name in df.
    pat : list
        Regular expression pattern with capturing groups.
    output_file:bool
        to output the result.
    label: str
        if output_file is True ,file label can change the name of output file.
    col_name:list
        col_name of result DataFrame.

    Returns
    -------
    result DataFrame with target.
    """
    pd.set_option('display.max_rows', 999)
    Length = len(df)
    df_mat = df[[target]].copy().drop_duplicates()
    match_ls, unique_ls, sample_ls = [],[],[]
    for idx,pattern in enumerate(pat):
        print(idx)
        if col_name:
            name = col_name[idx]
        else:
            name = 'result_{}'.format(idx)
        print('='*100,'\n','pattern:',pattern)
        df_mat[name] = df_mat[target].str.extract(pattern)
        print('match {} in {}'.format(len(df_mat[~df_mat[name].isnull()]),Length))
        print(df_mat[~df_mat[name].isnull()][target].head(),'\n')
        match_ls.append(len(df_mat[~df_mat[name].isnull()]))
        unique_ls.append(df_mat[name].unique())
        sample_ls.append(df_mat[~df_mat[name].isnull()][target].to_list())
    cols = df_mat.columns[1:].to_list()
    cols.extend([target])
    df_mat = df_mat[cols]
    df = df.merge(df_mat, how ='left')
    check = pd.DataFrame({'col_name':col_name, 'pattern':list(pat), 'match_count':match_ls, 'result_unique':unique_ls, 'sample':sample_ls})
    pd.reset_option('display.max_rows')
    if output_file:
        with pd.ExcelWriter('output/_temp_pat_result_%s.xlsx'%label, mode='a+') as writer:
            df.to_excel(writer, index=False, sheet_name='result') 
            check.to_excel(writer, index=False, sheet_name='check')
        # check.to_pickle('output/_temp_pat_result_%s.pkl'%label)
    return df

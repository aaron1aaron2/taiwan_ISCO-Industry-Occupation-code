import numpy as np
import pandas as pd
import pyreadstat
import re
import os
os.chdir('G:\共用雲端硬碟\資料科學小組\任務3_行職業文字轉ISCO_08代碼\cleandata')

from src.utils import get_allfile

def read_exportCSV(filepath:str ):
    '''
    這邊只處理SAV
    '''

    # ----sav
    if filepath.endswith('sav'):
        try:
            dt, meta  = pyreadstat.read_sav(filepath)
        except:
            try:
                dt ,meta = pyreadstat.read_sav(filepath,encoding = 'Big5-HKSCS') 
            except Exception as e:
                return {filepath:e}
        
        # label
        col = dt.columns
        value_lab = [] # 處理及插補value label
        for i in col:
            try:
                target = meta.variable_value_labels[i]
                target = {str(key):target[key] for key in target}
                str1 = str(target)
                #str1.replace(',',', \n')
            except :
                str1 = ''
        value_lab.append(str1)

        labelDF = pd.DataFrame(
            {'col_name': col,
            'col_lab': meta.column_labels,
            'val_lab': value_lab
            })

        labelDF.to_csv(re.sub( r"(?<=\.).*", 'label.csv', filepath), encoding='utf_8_sig',index=False)  

        dt.to_csv(re.sub( r"(?<=\.).*", 'csv', filepath), encoding='utf_8_sig',index=False)
  


if __name__ == "__main__":
  relSav_path = get_allfile(path ='..\\raw_data\\' , pat = r'.sav$', path_type = absolute)  
  print(relSav_path)
  for i in relSav_path:
    print(i)
    read_exportCSV(i)


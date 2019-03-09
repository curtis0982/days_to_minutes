# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 21:44:09 2018

@author: 張博鈞
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date,timedelta
import time, datetime,os


#此程式將日線模擬成分鐘線
#第1分=日開盤價，第2分=日最高價，第3分=日最低價，第4分~最後1分=日收盤價
#此開收盤時間設定為美國NYSE時間，請依需要自行調整

#read file
#請輸入日線資料路徑及檔案名稱
folder=r"D:\python_code\data\formc"
file_name="for_minute_trans_test.csv"


path = os.path.join(folder,file_name)
print(path)
df = pd.read_csv(path)
df['Date'] = pd.to_datetime(df["Date"])
df['Date'] = pd.to_datetime(df["Date"])
df_idx = df.set_index(["Date"], drop=True)

#把順序調換
df_idx = df_idx.sort_index(axis=1, ascending=True)
df_idx = df_idx.iloc[::-1]

#create iterator
def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

#create minute data list
dts=list()
for i in df_idx.index:
     for dt in datetime_range(( i + datetime.timedelta(minutes=570)), ( i + datetime.timedelta(minutes=961)), 
       timedelta(minutes=1)):
            if dt.strftime('%H:%M') == '09:30':
                dts.append([dt.strftime('%Y-%m-%d'),dt.strftime('%H:%M'),df_idx.loc[i]["Open"],
                           df_idx.loc[i]["Open"],df_idx.loc[i]["Open"],df_idx.loc[i]["Open"]])
            elif dt.strftime('%H:%M') == '09:31':
                dts.append([dt.strftime('%Y-%m-%d'),dt.strftime('%H:%M'),df_idx.loc[i]["High"],
                           df_idx.loc[i]["High"],df_idx.loc[i]["High"],df_idx.loc[i]["High"]])
            elif dt.strftime('%H:%M') == '09:32':
                dts.append([dt.strftime('%Y-%m-%d'),dt.strftime('%H:%M'),df_idx.loc[i]["Low"],
                           df_idx.loc[i]["Low"],df_idx.loc[i]["Low"],df_idx.loc[i]["Low"]])
            else:
                dts.append([dt.strftime('%Y-%m-%d'),dt.strftime('%H:%M'),df_idx.loc[i]["Close"],
                           df_idx.loc[i]["Close"],df_idx.loc[i]["Close"],df_idx.loc[i]["Close"]])
#put list into pd.df                        
minute_data =pd.DataFrame(dts,columns=['Date','Time','Open','High','Low','Close'])

#sort
minute_data.sort_values(["Date","Time"], inplace=True, ascending=True)  

#if(not(os.path.exists("Data_for_mc"))):
#os.makedirs("Data_for_mc")
out_path = r"D:\python_code\data\formc"
out_file_name ="m_"+file_name
out_path = os.path.join(out_path,out_file_name)
minute_data.to_csv(out_path, mode='w', header=True, index=False)

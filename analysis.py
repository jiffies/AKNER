#! -*- coding:utf-8 -*-
import pandas as pd
import csv

if __name__ == "__main__":
    for i in range(5):
        df = pd.read_csv('result/result'+str(i),sep='\t',header=None,quoting=csv.QUOTE_NONE)
        df['error'] =df[4]!=df[5] 
        error = df
        error.to_csv('result/error'+str(i),sep='\t',header=False)


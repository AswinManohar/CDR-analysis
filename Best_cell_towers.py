#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import re
import sys
import time


start = time.time()
new_cdr_data = pd.ExcelFile('dboutput100k.xlsx')
cdr_new = new_cdr_data.parse('dboutput')
cdr_for_analysis = cdr_new.head(100)

df = cdr_for_analysis[['xbin', 'ybin']]
measurmeents = cdr_for_analysis['measurements']

fd = cdr_for_analysis[['xbin','ybin','measurements']]
fd_meaurements = fd['measurements']



def tidy_split(df, column, sep='|', keep=False):
    """
    Split the values of a column and expand so the new DataFrame has one split
    value per row. Filters rows where the column is missing.

    Params
    ------
    df : pandas.DataFrame
        dataframe with the column to split and expand
    column : str
        the column to split and expand
    sep : str
        the string used to split the column's values
    keep : bool
        whether to retain the presplit value as it's own row

    Returns
    -------
    pandas.DataFrame
        Returns a dataframe with the same columns as `df`.
    """
    indexes = list()
    new_values = list()
    df = df.dropna(subset=[column])
    for i, presplit in enumerate(df[column].astype(str)):
        values = presplit.split(sep)
        if keep and len(values) > 1:
            indexes.append(i)
            new_values.append(presplit)
        for value in values:
            indexes.append(i)
            new_values.append(value)
    new_df = df.iloc[indexes, :].copy()
    new_df[column] = new_values
    new_df 
    return new_df



final = tidy_split(fd, 'measurements', sep=('},{'))
final['measurements'] = final['measurements'].map(lambda x: x.lstrip('+{[:').rstrip('rsrp'))
che=final.reset_index()
foo = lambda x: pd.Series([i for i in reversed(x.split(','))])
rev = che['measurements'].apply(foo)
rev.rename(columns={0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',8:'rsrp',9:'j',10:'Itecelloid'},inplace=True)
rev = rev[['a','b','c','d','e','f','g','h','rsrp','j','Itecelloid']]
che['itecelloid'] = rev['Itecelloid'].values 
che['rsrp'] = rev['rsrp'].values
che['itecelloid'] = che['itecelloid'].astype(str).str.replace('\D+', '')
che['rsrp'] = che['rsrp'].astype(str).str.replace('rsrp:','')
che= che.dropna(subset=['rsrp'])
final_che= che[["xbin","ybin","itecelloid","rsrp"]]
A = final_che[final_che['itecelloid'].astype(bool)]
grouped = A.groupby(['xbin','ybin'])


grouped = A.groupby(['xbin','ybin'])

for name,group in grouped:
    print(name)
    #print(group)
    group['rsrp'] = pd.to_numeric(group['rsrp'])
    g = group.groupby(['itecelloid'],as_index=False).agg({'rsrp': 'mean'})
    print (g)
    if not g.empty:
       print ("Data available")
       maxi = g.loc[g['rsrp'].idxmax()]

        
        

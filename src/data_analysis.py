# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     data_analysis
   Description :   分析特征
   Author :        wrm
   date：          2017/12/19
"""
__author__ = 'wrm'

import pandas as pd
import numpy as np

train_data = pd.read_csv('../data/prepare_data.csv')
train_data.get_dtype_counts()
# float64    2448
# int64       912
# object       11

is_object = train_data.dtypes == object
col_object = is_object[is_object]
print(col_object.index)
# Index(['ID', 'TOOL_ID', 'Tool', 'TOOL_ID (#1)', 'TOOL_ID (#2)', 'TOOL_ID (#3)',
#       'Tool (#2)', 'tool (#1)', 'TOOL', 'TOOL (#1)', 'TOOL (#2)'],
#      dtype='object')

for obj in list(col_object.index)[1:]:
    print(pd.value_counts(train_data[obj]))
    print()

remove_object = train_data.drop(list(col_object.index), axis=1)
corr = np.nan_to_num(np.corrcoef(remove_object, rowvar=0)[-1, :-1])
print("CORR_MAX = %f, CORR_MIN = %f" % (corr.max(), corr.min()))
# CORR_MAX = 0.262535, CORR_MIN = -0.308339


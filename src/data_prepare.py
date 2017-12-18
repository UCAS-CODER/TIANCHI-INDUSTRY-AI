# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     data_prepare
   Description :   数据分析与清洗
   Author :        wrm
   date：          2017/12/18
"""
__author__ = 'wrm'

import numpy as np
import pandas as pd

train_data = pd.read_excel('../data/训练.xlsx')

# 用于判断是否存在列，其中每个元素都相同或为NaN，没有无用的列
# for i in range(1, train_data.shape[1]):
#    if pd.value_counts(train_data.iloc[:, 1]).shape[0] <= 2:
#        print('row i is duplicated! line name is %s' % train_data.columns[i])

isDuplicated = train_data.T.duplicated()
# 计算重复的列的数量，结果重复的为4571列，不重复的列为3458列
# isDuplicated.value_counts()

# 去掉重复的列
train_data = train_data.iloc[:, [i for i in range(train_data.shape[1]) if not isDuplicated[i]]]

# 用于统计每一个元素的缺失值数量，最多的为381个，由于共3458列，可以接受
# nan_num_list = []
# for i in range(train_data.shape[0]):
#    # 统计每一个样本的缺失值数量
#    nan_num = pd.value_counts(train_data.isnull().iloc[i,:])[1]
#    nan_num_list.append(nan_num)
# max(nan_num_list) # 381

# 用于统计每一列的缺失值数量，最多的为500个，全部缺失，没有缺失值的列为2809列
#nan_num_list = []
#for i in range(train_data.shape[1]):
#    # 统计每一个列的缺失值数量
#    nan_num = pd.value_counts(train_data.isnull().iloc[:, i]).get(1, 0)
#    nan_num_list.append(nan_num)
#max(nan_num_list) # 500
#nan_num_list.count(0) # 2809

# 仅保留非nan值超过300的列，剩余3371列，改为400也是同样的结果
# 如果把thresh=200，则剩余3457列，仅去掉全缺失的列
train_data = train_data.dropna(axis=1, how='any', thresh=300)

# 用前一个未缺失值填补缺失值，bfill:后一个，None:额外指定value去填补缺失值
train_data = train_data.fillna(method='ffill')

train_data.to_csv('../data/prepare_data.csv')
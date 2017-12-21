# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     xgboost
   Description :
   Author :        wrm
   date：          2017/12/21
"""
__author__ = 'wrm'


import xgboost as xgb
import pandas as pd
import time
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
import os
mingw_path = 'D:\\Program Files\\mingw-w64\\x86_64-7.2.0-posix-seh-rt_v5-rev0\\mingw64\\bin'
os.environ['PATH'] = mingw_path + ';' + os.environ['PATH']

train_data = pd.read_csv('../data/prepare_data.csv')
test_data_A = pd.read_csv('../data/test_A.csv')
is_object = train_data.dtypes == object
col_object = is_object[is_object]
remove_object = train_data.drop(list(col_object.index), axis=1)
test_data_A = test_data_A.drop(list(col_object.index), axis=1)
data_np = np.matrix(remove_object.as_matrix())
train_np = data_np[:, :-1]
label_np = data_np[:, -1]
test_np = np.matrix(test_data_A.as_matrix())

min_max_scaler = preprocessing.MinMaxScaler()
train_minmax = min_max_scaler.fit_transform(train_np)
test_minmax = min_max_scaler.transform(test_np)

X_train, X_valid, y_train, y_valid = train_test_split(train_minmax, label_np, test_size=0.2, random_state=42)
xgtrain = xgb.DMatrix(X_train, y_train)
xgval = xgb.DMatrix(X_valid, y_valid)
xgtest = xgb.DMatrix(test_minmax)

watchlist = [(xgtrain, 'train'),(xgval, 'val')]

# 正式进入xgboost模型
params={
'booster':'gbtree',
'objective': 'reg:linear',
'gamma':0.3,  # 在树的叶子节点下一个分区的最小损失，越大算法模型越保守 。[0:]
'max_depth':6 , # 构建树的深度 [1:]
'lambda':0.1,  # L2 正则项权重
'alpha':0,
'subsample':0.5, # 采样训练数据，设置为0.5，随机选择一般的数据实例 (0:1]
'colsample_bytree':1, # 构建树树时的采样比率 (0:1]
'min_child_weight':25, # 节点的最少特征数
'eval_metric':'rmse',
#'missing': 0,
'eta': 0.1, # 如同学习率
'seed':710,
#'nthread':4,# cpu 线程数,根据自己U的个数适当调整
}
plst = list(params.items())
num_rounds = 5000  # 拟迭代次数

# 训练模型
model = xgb.train(plst, xgtrain, num_rounds, watchlist, early_stopping_rounds=100)
savetime = time.strftime('%m%d_%H_%M',time.localtime(time.time()))
model.save_model('../model/xgb_'+ savetime +'.model')  # 用于存储训练出的模型

preds = model.predict(xgtest,ntree_limit=model.best_iteration)

submit_template_file = open('../data/测试A-答案模板.csv')
submit_file = open('../submission/submission_' + savetime + '.csv', 'w')
i = 0
for line in submit_template_file.readlines():
    out_line = line[:-1] + ',' + str(preds[i]) + '\n'
    submit_file.write(out_line)
    i += 1
submit_file.close()

# 定义规则，预测值为训练数据中相同TOOL_ID的平均数
dict_TOOL_ID = {}
TOOL_ID_type = list(pd.value_counts(train_data[list(col_object.index)[1]]).index)
for type in TOOL_ID_type:
    dict_TOOL_ID[type] = np.mean(train_data[train_data[list(col_object.index)[1]] == type]['Y'])
pred_TOOL_ID = list(range(len(test_data_A)))
for i in range(len(test_data_A)):
    pred_TOOL_ID[i] = dict_TOOL_ID[test_data_A[list(col_object.index)[1]][i]]
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     linear regression
   Description :
   Author :        wrm
   date：          2017/12/19
"""
__author__ = 'wrm'

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
import time

train_data = pd.read_csv('../data/prepare_data.csv')
test_data_A = pd.read_excel('../data/test_A.csv')
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

lr_model = LinearRegression()
lr_model.fit(train_minmax, label_np)
predict = lr_model.predict(test_minmax)
p_m = predict.mean()
p_v = predict.var()
t_m = label_np.mean()
t_v = label_np.var()
print("预测均值为%f, 方差为%f" % (p_m, p_v))

predict_norm = t_m + (predict - p_m) / (p_v / t_v) ** 0.5
for i in range(len(predict_norm)):
    if predict_norm[i] > label_np.max():
        predict_norm[i] = label_np.max()
    elif predict_norm[i] < label_np.min():
        predict_norm[i] = label_np.min()

submit_template_file = open('../data/测试A-答案模板.csv')
save_time = time.strftime('%m%d_%H_%M', time.localtime(time.time()))
submit_file = open('../submission/submission_' + save_time + '.csv', 'w')
i = 0
for line in submit_template_file.readlines():
    out_line = line[:-1] + ',' + str(predict_norm[i][0]) + '\n'
    submit_file.write(out_line)
    i += 1
submit_file.close()

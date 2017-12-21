# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     submit
   Description :   一个简单的提交样例
   Author :        wrm
   date：          2017/12/18
"""
__author__ = 'wrm'

import time

submit_template_file = open('../data/测试A-答案模板.csv')
save_time = time.strftime('%m%d_%H_%M', time.localtime(time.time()))
submit_file = open('../submission/submission_' + save_time + '.csv', 'w')
for line in submit_template_file.readlines():
    out_line = line[:-1] + ',' + str(2.846187) + '\n'
    submit_file.write(out_line)

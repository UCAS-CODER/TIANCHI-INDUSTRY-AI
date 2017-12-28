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


def submit(preds, out_file=None):
    """
    生成提交的文件
    :param preds: 两列：ID，预测值
    :param out_file: 输出的文件，不输入则使用加时间的默认值
    :return: None
    """
    if out_file is None:
        save_time = time.strftime('%m%d_%H_%M', time.localtime(time.time()))
        submit_file = open('../submission/submission_' + save_time + '.csv', 'w')
    else:
        submit_file = open(out_file, 'w')
    for row in preds:
        out_line = str(row[0]) + ',' + str(row[1]) + '\n'
        submit_file.write(out_line)
    submit_file.close()



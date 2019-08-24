# -*- coding: UTF-8 -*-

import time
import preprocess

SOURCEPATH = './data/meterId5081.csv'
# TARGETPATH = './result/meterId7048_aggregation.csv'

if __name__ == '__main__':
	# 获取开始时间
	startTime = time.time()

	# 对文件数据进行聚类，将每小时、每天、每月的数据分别放入不同文件。
	# preprocess.aggregate(SOURCEPATH)
	preprocess.aggregate_iterator(SOURCEPATH)
	
	# 获取结束时间
	endTime = time.time()
	
	# 计算程序用时
	print "Total time: ", endTime - startTime

# -*- coding: UTF-8 -*-

import time
import preprocess
import os

# SOURCEFOLDER = './data/xj_mdm/test/'
SOURCEFOLDER = './data/xj_mdm/collection_record/'
TARGETFOLDER = './result/xj_result/'

if __name__ == '__main__':
	# 获取开始时间
	startTime = time.time()

	# 聚合文件夹中所有文件
	files = os.listdir(SOURCEFOLDER)
	for f in files:
		print f
		preprocess.aggregate_iterator_allin(SOURCEFOLDER + f, TARGETFOLDER + f)

	# 聚合单个文件，用于调试
	# f = 'meterId130325000017.csv'
	# preprocess.aggregate(SOURCEPATH)
	# preprocess.aggregate_iterator(SOURCEPATH)
	# preprocess.aggregate_iterator_allin(SOURCEFOLDER + f, TARGETFOLDER + f)

	# 获取结束时间
	endTime = time.time()
	
	# 计算程序用时
	print "Total time: ", endTime - startTime

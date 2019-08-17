# -*- coding: UTF-8 -*-

import pandas as pd

def aggregate(strPath, targetPath):

	# 输出列表数据结构
	startDateList = []
	endDateList = []
	gasDiffList = []

	# 将csv文件读入为数据帧格式
	dfInput = pd.read_csv(strPath)

	# 遍历数据帧，构造数据输出列表
	for row in range(1, len(dfInput)):
		print dfInput.iloc[row]['Data_Date'], dfInput.iloc[row]['Working_Sum']
		gasDiff = dfInput.iloc[row]['Working_Sum'] - dfInput.iloc[row-1]['Working_Sum']
		startDateList.append(dfInput.iloc[row-1]['Data_Date'])
		endDateList.append(dfInput.iloc[row]['Data_Date'])
		gasDiffList.append(gasDiff)
	
	# 创建输出数据帧
	aggreData = {'Start_Date': startDateList, 'End_Date': endDateList, 'Gas_Diff': gasDiffList}
	dfOutput = pd.DataFrame(aggreData)
	dfOutput.to_csv(targetPath, encoding="utf_8_sig")

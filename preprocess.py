# -*- coding: UTF-8 -*-

import time
import pandas as pd

def aggregate(strPath):
	# 输出列表数据结构
	startHourList = []
	endHourList = []
	hourSumList = []
	startDayList = []
	endDayList = []
	daySumList = []
	startMonthList = []
	endMonthList = []
	monthSumList = []

	startRead = time.time()
	# 将csv文件读入为数据帧格式
	dfInput = pd.read_csv(strPath)
	endRead = time.time()
	# 计算读文件用时
	print "read time: ", endRead - startRead

	startTransform = time.time()
	# 将时间信息转换格式
	dfInput['Data_Date'] = pd.to_datetime(dfInput['Data_Date'], format="%Y/%m/%d %H:%M:%S")
	endTransform = time.time()
	# 计算格式化数据用时
	print "Transform time: ", endTransform - startTransform

	# 取第一条数据作为临时数据，此后该变量暂存，小时、日、月起始时间和用气量
	hourTemp = dfInput.iloc[0]['Data_Date']
	dayTemp = dfInput.iloc[0]['Data_Date']
	monthTemp = dfInput.iloc[0]['Data_Date']
	hourSumTemp = dfInput.iloc[0]['Working_Sum']
	daySumTemp = dfInput.iloc[0]['Working_Sum']
	monthSumTemp = dfInput.iloc[0]['Working_Sum']
	
	startTraverse = time.time()
	# 遍历整个数据帧
	for row in range(1, len(dfInput)):
		# 本行数据减去上一条数据，获得小时的时间差，天时间差，月时间差
		hourDiff = dfInput.iloc[row]['Data_Date'].hour - dfInput.iloc[row - 1]['Data_Date'].hour
		dayDiff = dfInput.iloc[row]['Data_Date'].day - dfInput.iloc[row - 1]['Data_Date'].day
		monthDiff = dfInput.iloc[row]['Data_Date'].month - dfInput.iloc[row - 1]['Data_Date'].month
		# 判断小时的时间差，如果时间差不是0，说明进入新的小时，将此数据输出到对应list
		if hourDiff != 0:
			# print "new hour"
			startHourList.append(hourTemp)
			endHourList.append(dfInput.iloc[row]['Data_Date'])
			hourGasDiff = dfInput.iloc[row]['Working_Sum'] - hourSumTemp
			hourSumList.append(hourGasDiff)
			hourTemp = dfInput.iloc[row]['Data_Date']
			hourSumTemp = dfInput.iloc[row]['Working_Sum']
		# 判断天的时间差，如果时间差不是0，说明进入新的一天，将此数据输出到对应list
		if dayDiff != 0:
			# print "new day"
			startDayList.append(dayTemp)
			endDayList.append(dfInput.iloc[row]['Data_Date'])
			dayGasDiff = dfInput.iloc[row]['Working_Sum'] - daySumTemp
			daySumList.append(dayGasDiff)
			dayTemp = dfInput.iloc[row]['Data_Date']
			daySumTemp = dfInput.iloc[row]['Working_Sum']
		# 判断月的时间差，如果时间差不是0，说明进入新的月份，将此数据输出到对应list
		if monthDiff != 0:
			# print "new month"
			startMonthList.append(monthTemp)
			endMonthList.append(dfInput.iloc[row]['Data_Date'])
			monthGasDiff = dfInput.iloc[row]['Working_Sum'] - monthSumTemp
			monthSumList.append(monthGasDiff)
			monthTemp = dfInput.iloc[row]['Data_Date']
			monthSumTemp = dfInput.iloc[row]['Working_Sum']
	endTraverse = time.time()
	# 计算遍历用时
	print "Traverse time: ", endTraverse - startTraverse

	startOutput = time.time()
	# 构造输出的小时信息的数据帧和输出文件
	hourData = {'Start_Date': startHourList, 'End_Date': endHourList, 'Gas_Diff': hourSumList}
	dfHourOutput = pd.DataFrame(hourData)
	dfHourOutput.to_csv('./result/hour.csv', encoding="utf_8_sig")
	# 构造输出的日信息的数据帧和输出文件
	dayData = {'Start_Date': startDayList, 'End_Date': endDayList, 'Gas_Diff': daySumList}
	dfDayOutput = pd.DataFrame(dayData)
	dfDayOutput.to_csv('./result/day.csv', encoding="utf_8_sig")
	# 构造输出的月信息的数据帧和输出文件
	monthData = {'Start_Date': startMonthList, 'End_Date': endMonthList, 'Gas_Diff': monthSumList}
	dfMonthOutput = pd.DataFrame(monthData)
	dfMonthOutput.to_csv('./result/month.csv', encoding="utf_8_sig")
	endOutput = time.time()
	# 计算输出用时
	print "Output time: ", endOutput - startOutput

def aggregate_iterator(strPath):
	# 输出列表数据结构
	startHourList = []
	endHourList = []
	hourSumList = []
	startDayList = []
	endDayList = []
	daySumList = []
	startMonthList = []
	endMonthList = []
	monthSumList = []

	# 将csv文件读入为数据帧格式
	dfInput = pd.read_csv(strPath)
	
	# 将时间信息转换格式
	dfInput['Data_Date'] = pd.to_datetime(dfInput['Data_Date'], format="%Y/%m/%d %H:%M:%S")

	# 取第一条数据作为临时数据，此后该变量暂存，小时、日、月起始时间和用气量
	hourTemp = dfInput.iloc[0]['Data_Date']
	dayTemp = dfInput.iloc[0]['Data_Date']
	monthTemp = dfInput.iloc[0]['Data_Date']
	hourSumTemp = dfInput.iloc[0]['Working_Sum']
	daySumTemp = dfInput.iloc[0]['Working_Sum']
	monthSumTemp = dfInput.iloc[0]['Working_Sum']
	
	count = 0
	# 遍历
	for row in dfInput.itertuples():

		if count != 0:
			# 本行数据减去上一条数据，获得小时的时间差，天时间差，月时间差
			hourDiff = row[2].hour - hourTemp.hour
			dayDiff = row[2].day - dayTemp.day
			monthDiff = row[2].month - monthTemp.month
			# 判断小时的时间差，如果时间差不是0，说明进入新的小时，将此数据输出到对应list
			if hourDiff != 0:
				# print "new hour"
				startHourList.append(hourTemp)
				endHourList.append(row[2])
				hourGasDiff = row[9] - hourSumTemp
				hourSumList.append(hourGasDiff)
				hourTemp = row[2]
				hourSumTemp = row[9]
			# 判断天的时间差，如果时间差不是0，说明进入新的一天，将此数据输出到对应list
			if dayDiff != 0:
				# print "new day"
				startDayList.append(dayTemp)
				endDayList.append(row[2])
				dayGasDiff = row[9] - daySumTemp
				daySumList.append(dayGasDiff)
				dayTemp = row[2]
				daySumTemp = row[9]
			# 判断月的时间差，如果时间差不是0，说明进入新的月份，将此数据输出到对应list
			if monthDiff != 0:
				# print "new month"
				startMonthList.append(monthTemp)
				endMonthList.append(row[2])
				monthGasDiff = row[9] - monthSumTemp
				monthSumList.append(monthGasDiff)
				monthTemp = row[2]
				monthSumTemp = row[9]
		count += 1

	# 构造输出的小时信息的数据帧和输出文件
	hourData = {'Start_Date': startHourList, 'End_Date': endHourList, 'Gas_Diff': hourSumList}
	dfHourOutput = pd.DataFrame(hourData)
	dfHourOutput.to_csv('./result/hour.csv', encoding="utf_8_sig")
	# 构造输出的日信息的数据帧和输出文件
	dayData = {'Start_Date': startDayList, 'End_Date': endDayList, 'Gas_Diff': daySumList}
	dfDayOutput = pd.DataFrame(dayData)
	dfDayOutput.to_csv('./result/day.csv', encoding="utf_8_sig")
	# 构造输出的月信息的数据帧和输出文件
	monthData = {'Start_Date': startMonthList, 'End_Date': endMonthList, 'Gas_Diff': monthSumList}
	dfMonthOutput = pd.DataFrame(monthData)
	dfMonthOutput.to_csv('./result/month.csv', encoding="utf_8_sig")

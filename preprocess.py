# -*- coding: UTF-8 -*-

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
	# 将csv文件读入为数据帧格式
	dfInput = pd.read_csv(strPath)
	# 将时间信息转换格式
	dfInput['Data_Date'] = pd.to_datetime(dfInput['Data_Date'], format="%Y/%m/%d %H:%M:%S")
	# 取第一条数据作为临时数据，此后该变量暂存，小时、日、月起始时间和用气量
	hourTemp = dfInput.Data_Date[0]
	dayTemp = dfInput.Data_Date[0]
	monthTemp = dfInput.Data_Date[0]
	hourSumTemp = dfInput.Working_Sum[0]
	daySumTemp = dfInput.Working_Sum[0]
	monthSumTemp = dfInput.Working_Sum[0]
	# 遍历整个数据帧
	for row in range(1, len(dfInput)):
		# 本行数据减去上一条数据，获得小时的时间差，天时间差，月时间差
		hourDiff = dfInput.Data_Date.dt.hour[row] - dfInput.Data_Date.dt.hour[row - 1]
		dayDiff = dfInput.Data_Date.dt.day[row] - dfInput.Data_Date.dt.day[row - 1]
		monthDiff = dfInput.Data_Date.dt.month[row] - dfInput.Data_Date.dt.month[row - 1]
		# 判断小时的时间差，如果时间差不是0，说明进入新的小时，将此数据输出到对应list
		if hourDiff != 0:
			print "new hour"
			startHourList.append(hourTemp)
			endHourList.append(dfInput.Data_Date[row])
			hourGasDiff = dfInput.Working_Sum[row] - hourSumTemp
			hourSumList.append(hourGasDiff)
			hourTemp = dfInput.Data_Date[row]
			hourSumTemp = dfInput.Working_Sum[row]
		# 判断天的时间差，如果时间差不是0，说明进入新的一天，将此数据输出到对应list
		if dayDiff != 0:
			print "new day"
			startDayList.append(dayTemp)
			endDayList.append(dfInput.Data_Date[row])
			dayGasDiff = dfInput.Working_Sum[row] - daySumTemp
			daySumList.append(dayGasDiff)
			dayTemp = dfInput.Data_Date[row]
			daySumTemp = dfInput.Working_Sum[row]
		# 判断月的时间差，如果时间差不是0，说明进入新的月份，将此数据输出到对应list
		if monthDiff != 0:
			print "new month"
			startMonthList.append(monthTemp)
			endMonthList.append(dfInput.Data_Date[row])
			monthGasDiff = dfInput.Working_Sum[row] - monthSumTemp
			monthSumList.append(monthGasDiff)
			monthTemp = dfInput.Data_Date[row]
			monthSumTemp = dfInput.Working_Sum[row]

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
	


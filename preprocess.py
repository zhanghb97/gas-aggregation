# -*- coding: UTF-8 -*-

import time
import pandas as pd
import random

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
	hourTemp = dfInput.iloc[0]['Data_Date']
	dayTemp = dfInput.iloc[0]['Data_Date']
	monthTemp = dfInput.iloc[0]['Data_Date']
	hourSumTemp = dfInput.iloc[0]['Working_Sum']
	daySumTemp = dfInput.iloc[0]['Working_Sum']
	monthSumTemp = dfInput.iloc[0]['Working_Sum']
	
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

# 聚合函数，并输出标准格式文件
def aggregate_iterator_allin(strPath, targetPath):
	# 小时，日，月时间及用气量列表
	startHourList = []
	endHourList = []
	hourSumList = []
	startDayList = []
	endDayList = []
	daySumList = []
	startMonthList = []
	endMonthList = []
	monthSumList = []	
	hourGasStart = []
	hourGasEnd = []
	dayGasStart = []
	dayGasEnd = []
	monthGasStart = []
	monthGasEnd = []

	# 输出的聚合结果，起始时间结果，起始用气量结果
	resultList = []
	startList = []
	endList = []
	startGasList = []
	endGasList = []

	# meter_id, meter_no, tenant_id, am_id列表
	meterIdList = []
	meterNoList = []
	tenantIdList = []
	amIdList = []

	# 粒度数值，可根据实际需要修改
	hourGranularity = 2
	dayGranularity = 3
	monthGranularity = 4

	# 粒度列表，分为小时、天、月的粒度列表，最后汇总在一起
	hourGranularityList = []
	dayGranularityList = []
	monthGranularityList = []
	timeGranularityList = []

	# 将csv文件读入为数据帧格式
	dfInput = pd.read_csv(strPath, error_bad_lines=False)
	
	# 将时间信息转换格式
	try:
		dfInput['data_time'] = pd.to_datetime(dfInput['data_time'], format="%Y/%m/%d %H:%M:%S")
	except ValueError:
		print strPath
	else:
		print "Finish to_datetime!"

	# 取第一条数据作为临时数据，此后该变量暂存，小时、日、月起始时间和用气量
	hourTemp = dfInput.iloc[0]['data_time']
	dayTemp = dfInput.iloc[0]['data_time']
	monthTemp = dfInput.iloc[0]['data_time']
	hourSumTemp = dfInput.iloc[0]['standard_num']
	daySumTemp = dfInput.iloc[0]['standard_num']
	monthSumTemp = dfInput.iloc[0]['standard_num']

	# 取meter_id, meter_no, tenant_id
	meterId = dfInput.iloc[0]['meter_id']
	meterNo = dfInput.iloc[0]['meter_no']
	tenantId = dfInput.iloc[0]['tenant_id']
	
	count = 0
	# 遍历数据帧
	for row in dfInput.itertuples():
		try:
			if count != 0:
				# 本行数据减去上一条数据，获得小时的时间差，天时间差，月时间差
				hourDiff = row[3].hour - hourTemp.hour
				dayDiff = row[3].day - dayTemp.day
				monthDiff = row[3].month - monthTemp.month
				# 判断小时的时间差，如果时间差不是0，说明进入新的小时，将此数据输出到对应list
				if hourDiff != 0:
					startHourList.append(hourTemp)
					endHourList.append(row[3])
					hourGasDiff = row[10] - hourSumTemp
					hourGasStart.append(hourSumTemp)
					hourGasEnd.append(row[10])
					hourSumList.append(hourGasDiff)
					meterIdList.append(meterId)
					meterNoList.append(meterNo)
					tenantIdList.append(tenantId)
					hourGranularityList.append(hourGranularity)
					# 构造主键
					amIdList.append(primary_key())
					hourTemp = row[3]
					hourSumTemp = row[10]
				# 判断天的时间差，如果时间差不是0，说明进入新的一天，将此数据输出到对应list
				if dayDiff != 0:
					startDayList.append(dayTemp)
					endDayList.append(row[3])
					dayGasDiff = row[10] - daySumTemp
					dayGasStart.append(daySumTemp)
					dayGasEnd.append(row[10])
					daySumList.append(dayGasDiff)
					meterIdList.append(meterId)
					meterNoList.append(meterNo)
					tenantIdList.append(tenantId)
					dayGranularityList.append(dayGranularity)
					# 构造主键
					amIdList.append(primary_key())
					dayTemp = row[3]
					daySumTemp = row[10]
				# 判断月的时间差，如果时间差不是0，说明进入新的月份，将此数据输出到对应list
				if monthDiff != 0:
					startMonthList.append(monthTemp)
					endMonthList.append(row[3])
					monthGasDiff = row[10] - monthSumTemp
					monthGasStart.append(monthSumTemp)
					monthGasEnd.append(row[10])
					monthSumList.append(monthGasDiff)
					meterIdList.append(meterId)
					meterNoList.append(meterNo)
					tenantIdList.append(tenantId)
					monthGranularityList.append(monthGranularity)
					# 构造主键
					amIdList.append(primary_key())
					monthTemp = row[3]
					monthSumTemp = row[10]
			count += 1
		except AttributeError:
			print row[3]
			print "AttributeError"

	# 构造输出的聚合结果、起始时间、起始用气量列表
	resultList = hourSumList + daySumList + monthSumList
	startList = startHourList + startDayList + startMonthList
	endList = endHourList + endDayList + endMonthList
	startGasList = hourGasStart + dayGasStart + monthGasStart
	endGasList = hourGasEnd + dayGasEnd + monthGasEnd
	timeGranularityList = hourGranularityList + dayGranularityList + monthGranularityList

	# 构造输出数据帧
	resultData = {'am_id': amIdList, 'time_granularity': timeGranularityList, 'tenant_id': tenantIdList, 
				  'meter_id': meterIdList,'meter_no': meterNoList, 'begin_time': startList, 'end_time': endList, 
				  'standard_qty': resultList, 'begin_standard_num': startGasList, 'end_standard_num': endGasList}
	resultOutput = pd.DataFrame(resultData)
	resultOutput["cust_id"] = ""
	resultOutput["begin_working_num"] = ""
	resultOutput["end_working_num"] = ""
	resultOutput["working_qty"] = ""
	resultOutput["am_state"] = 1
	# 输出到csv文件
	resultOutput.to_csv(targetPath, encoding = "utf_8_sig", index = None)

# 构造am_id主键数据
def primary_key():
	localtime = time.localtime(time.time())
	keyResult = ""
	# 添加年信息
	keyResult += str(localtime.tm_year)
	# 添加月信息
	if localtime.tm_mon < 10:
		keyResult = keyResult + "0" + str(localtime.tm_mon)
	else:
		keyResult += str(localtime.tm_mon)
	# 添加日信息
	if localtime.tm_mday < 10:
		keyResult = keyResult + "0" + str(localtime.tm_mday)
	else:
		keyResult += str(localtime.tm_mday)
	# 添加时信息
	if localtime.tm_hour < 10:
		keyResult = keyResult + "0" + str(localtime.tm_hour)
	else:
		keyResult += str(localtime.tm_hour)
	# 添加分信息
	if localtime.tm_min < 10:
		keyResult = keyResult + "0" + str(localtime.tm_min)
	else:
		keyResult += str(localtime.tm_min)
	# 添加秒信息
	if localtime.tm_sec < 10:
		keyResult = keyResult + "0" + str(localtime.tm_sec)
	else:
		keyResult += str(localtime.tm_sec)
	# 添加随机数信息
	keyResult += str(random.randint(0,999999))

	return keyResult 

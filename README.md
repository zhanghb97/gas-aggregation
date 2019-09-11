# gas-aggregation

本仓库实现产生燃气数据的聚合信息。

## 1. 筛选、聚合数据

采集信息频率分为：

- 两分钟一次
- 三分钟一次
- 五分钟一次
- 一小时一次
- 两小时一次
- 四小时一次
- 一天四次
- 一天两次
- 一天一次

### 1.1 筛选、聚合数据算法

本算法实现将燃气数据进行每小时、每天、每月进行分类，并进行聚合。

- 将燃气数据导入构造相应数据帧
- 将时间信息转换成标准格式
- 将第一条数据放入临时变量作为起始标准
- 遍历数据帧，分别取出当前数据的小时、天、月信息，与临时变量的信息进行比对
- 判断是否进入了新的小时、新的天、新的月
- 若进入了新的的小时、新的天、新的月，将相应时间信息加入list
- 用当前用气量减去临时变量中的用气量算出聚合数据，加入相应list
- 将list组合构造数据帧，并输出到`.csv`文件

### 1.2 取时间方法

时间信息经过`to_datetime`函数转换成标准格式，类型为时间戳类型。

取时间方法为先取行数据，再通过列名取时间戳数据，最后取小时、天、月信息。

例如：
```python
# 取第一条数据作为临时数据，此后该变量暂存，小时、日、月起始时间和用气量
hourTemp = dfInput.iloc[0]['Data_Date']
dayTemp = dfInput.iloc[0]['Data_Date']
monthTemp = dfInput.iloc[0]['Data_Date']
hourSumTemp = dfInput.iloc[0]['Working_Sum']
daySumTemp = dfInput.iloc[0]['Working_Sum']
monthSumTemp = dfInput.iloc[0]['Working_Sum']
```

通过测试，该方法比取数据帧列成员再取行信息的方法运行效率高。

在进行遍历时使用迭代器：

```python
for row in dfInput.itertuples():
	...
```

使用迭代器遍历数据帧无法改变数据帧的信息，不过可以获得更高的运行效率。

## 2. 使用方法

- 将原始数据放入`./data/xj_mdm／collection_record`文件夹中
- 通过注释的方法，在`./main.py`文件中，选择执行所有文件聚合或进行单个文件聚合(后续将会通过参数的方法进行完善)
- 在当前文件夹执行`python main.py`，聚合文件将会保存在`./result/xj_result`文件夹中
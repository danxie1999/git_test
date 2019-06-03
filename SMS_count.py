import os

##工作目录
DIR1 = os.getcwd()
##数据目录
DIR2 = os.path.join(DIR1,'data')

##如果没有数据目录，就报错退出
if os.path.exists(DIR2):
	pass
else:
	input('The {} does not exist,exiting...'.format(DIR2))
	exit()

##进入数据目录
os.chdir(DIR2)

##获取数据目录中的文件
L=os.listdir()


##过滤数据文件夹中符合条件的文件
import re
pattern1 = re.compile(r'CSS_Unicom_\d{8}.dat_cardid.csv')
pattern2 = re.compile(r'CSS_Unicom_\d{8}.dat_cardid.csv_dulcard.csv')

##文件名完全过滤
L_msg = [i for i in L if pattern1.match(i) != None and pattern1.match(i).group() == i]
L_sub = [i for i in L if pattern2.match(i) != None and pattern2.match(i).group() == i]



##如果没有发现相关文件，退出
if not L_msg or not L_sub:
	print('Cannot find required SMS files or duplicated files,exiting...')
	exit()

##获取当前月份
Time_Month = L_msg[0][11:17]

import pandas as pd

##操作函数
def conv_xlsx(List):
	## 定义输出execl文件名
	out_name = '{}_{}.xlsx'.format(List[0][0:17],re.split(r'[._]',List[0])[-2])
	## 定义输出文件名和目录
	out_file = os.path.join(DIR1,out_name)
	##创建一个空excel文件
	pd.DataFrame().to_excel(out_file)
	##创建一个pandas的excel的对象，这个目的是不让sheet_name覆盖原sheet_name
	writer = pd.ExcelWriter(out_file)
	###定义汇总df的列和图片名和汇总文件的名字
	Date_list = []
	msg_list = []
	sub_list = []
	pic_name = None
	sum_name = None
	##csv文件的合并成excel文件
	for msg in List:
		if msg.find('dulcard') >= 0:
			df = pd.read_csv(msg,header=None,names=['次数','卡号','卡状态'])
		else:
			df = pd.read_csv(msg,header=None,names=['日期','卡号','卡状态'])
			##短信数目
			msg_no = df['卡号'].count()
			##将一个df的短信数目和用户数传入对用的列表
			msg_list.append(msg_no)
			sub_list.append(df['卡号'].value_counts().size)

		##将日期传入对应列表
		Date=re.split(r'[._]',msg)[2]

		Date_list.append(Date)
		
		##将df转成excel文件
		df.to_excel(writer,index=0,sheet_name=Date)
	##保存和关闭excel对象
	writer.save()
	writer.close()
	##如果文件是短信数目
	if List[0].find('dulcard') < 0:
		##准备画图和制作汇总excel
		import matplotlib.pyplot as plt
		import matplotlib.dates as mdate
		##设置中文显示
		plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']#设置中文
		plt.rcParams['axes.unicode_minus'] = False

		##定义图片规格
		fig = plt.figure(figsize=(8,5))
		##定义一个轴对象
		ax = fig.add_subplot(111)
		#设置X轴的时间标记
		ax.xaxis.set_major_formatter(mdate.DateFormatter('%m%d'))
		fig.autofmt_xdate() #自动调整X轴格式
		##消除上边框和右边框
		ax.spines['right'].set_color('none')
		ax.spines['top'].set_color('none')

		##定义x,y轴，将x轴的数据转为时间类型		
		from datetime import datetime
		x = [datetime.strptime(i,'%Y%m%d')for i in Date_list]
		y1 = msg_list
		y2 = sub_list

		##画图
		plt.plot(x,y1,color='#9999ff',label='短信数')
		plt.plot(x,y2,color='#ff9999',label='订户数')
		##定义x,y轴的注释，和图标位置
		plt.xlabel(Time_Month)
		plt.ylabel('Numbers')
		plt.legend(loc='best')
		##保存图片
		pic_name = 'CSS_Unicom_{}.png'.format(Time_Month)
		plt.savefig(os.path.join(DIR1,pic_name))

		##每天的汇总数据
		df_sum = pd.DataFrame({'日期':Date_list,'用户个数':sub_list,'短信条数':msg_list},columns=['日期','用户个数','短信条数']).set_index('日期')

		##加入最后一行计算数据
		from functools import reduce	
		msg_sum = reduce(lambda x,y:x+y,msg_list)
		sub_sum = reduce(lambda x,y:x+y,sub_list)
		df_addrow = pd.DataFrame([['总数',sub_sum,msg_sum],],columns=['日期','用户个数','短信条数']).set_index('日期')

		##合并汇总数据和计算行
		df_sum = pd.concat([df_sum,df_addrow])

		df_sum.reset_index(inplace=True)
		##生成excel文件
		sum_name = 'CSS_Unicom_{}_Sum.xlsx'.format(Time_Month)
		df_sum.to_excel(os.path.join(DIR1,sum_name),index=0)
	return (out_name,pic_name,sum_name)		


if __name__ == '__main__':
	file_1,pic_name_1,sum_name_1 = conv_xlsx(L_msg)
	file_2,pic_name_2,sum_name_2 = conv_xlsx(L_sub)
	input('Mission completed!!!,please check following output files:\n{0}\\{1}\n{0}\\{2}\n{0}\\{3}\n{0}\\{4}\nexiting...'.format(DIR1,\
			file_1,file_2,sum_name_1,pic_name_1))


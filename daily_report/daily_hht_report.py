import pandas as pd
import numpy as np
import os


##工作目录
DIR1 = os.getcwd()
##数据目录
DIR2 = os.path.join(DIR1,'data')
##模板目录
DIR3 = os.path.join(DIR1,'template')

##如果没有数据目录，就报错退出
if os.path.exists(DIR2):
    pass
else:
    input('The {} does not exist,exiting...'.format(DIR2))
    exit()


def csv_report_excel(input_data):
    ##读取数据文件
    df_from =pd.read_csv(input_data,index_col='name')

    ##根据读取数据提取数据变量
    sub_create_p3 = int(df_from.loc['sub_create','p1/p3'])
    card_total_p3 = int(df_from.loc['card_total','p1/p3'])
    sub_create_p4 = int(df_from.loc['sub_create','p4'])
    card_total_p4 = int(df_from.loc['card_total','p4'])
    sub_create_cct = int(df_from.loc['sub_create','cct'])
    card_total_cct = int(df_from.loc['card_total','cct'])
    asa = int(df_from.loc['asa','p1/p3'])
    H_p3 = df_from.loc['H','p1/p3']
    A_p3 = df_from.loc['A','p1/p3']
    R_p3 = df_from.loc['R','p1/p3']

    H_p4 = df_from.loc['H','p4']
    A_p4 = df_from.loc['A','p4']
    R_p4 = df_from.loc['R','p4']

    H_cct = int(df_from.loc['H','cct'])

    bj_sub_create_p3 = int(df_from.loc['bj_sub_create','p1/p3'])
    utc_sub_create_m_p3 = int(df_from.loc['utc_sub_create_m','p1/p3'])
    utc_sub_del_m_p3 = int(df_from.loc['utc_sub_del_m','p1/p3'])
    utc_sub_create_a_p3 = int(df_from.loc['utc_sub_create_a','p1/p3'])
    utc_sub_del_a_p3 = int(df_from.loc['utc_sub_del_a','p1/p3'])

    bj_sub_create_p4 = int(df_from.loc['bj_sub_create','p4'])
    utc_sub_create_m_p4 = int(df_from.loc['utc_sub_create_m','p4'])
    utc_sub_del_m_p4 = int(df_from.loc['utc_sub_del_m','p4'])
    utc_sub_create_a_p4 = int(df_from.loc['utc_sub_create_a','p4'])
    utc_sub_del_a_p4 = int(df_from.loc['utc_sub_del_a','p4'])


    utc_sub_create_m_cct = int(df_from.loc['utc_sub_create_m','cct'])
    utc_sub_del_m_cct = int(df_from.loc['utc_sub_del_m','cct'])
    utc_sub_create_a_cct = int(df_from.loc['utc_sub_create_a','cct'])
    utc_sub_del_a_cct = int(df_from.loc['utc_sub_del_a','cct'])

    ##日期的处理
    Date = str(int(df_from.loc['Date','p1/p3']))
    from datetime import datetime,timedelta
    dt = datetime.strptime(Date,'%Y%m%d')
    dt_y = dt - timedelta(days=1)
    week_lookup = {'1':'周一','2':'周二','3':'周三','4':'周四','5':'周五','6':'周六','0':'周日'}
    week_day = week_lookup[dt.strftime('%w')]
    dt_str = dt.strftime('%m{}%d{}').format('月','日')
    dt_y_str = dt_y.strftime('%m{}%d{}').format('月','日')
    monday = dt - timedelta(days=dt.weekday()) 
    sunday = dt + timedelta(days=6 - dt.weekday()) 



    ##模板生成数据
    template_col = os.path.join(DIR3,'temp.plk')

    temp = pd.read_pickle(template_col)
    ##星期
    temp[2] = week_day
    ##hht p3 
    temp[7] = '户户通(P1/P3)用户数:       {:,}\n户户通(P1/P3)智能卡总量:    {:,}'.format(sub_create_p3,card_total_p3)
    ##hht p4
    temp[8] = '户户通(P3/P4/P5)用户数:     {:,}\n户户通(P3/P4/P5)智能卡总量:  {:,}'.format(sub_create_p4,card_total_p4)
    ##cct
    temp[9] = '村村通用户数:              {:,}\n村村通智能卡总量:         {:,}'.format(sub_create_cct,card_total_cct)
    ##ASA connections
    temp[10] = asa
    ##hhtp3 带宽
    temp[11] = '户户通(P1/P3): (可用带宽1000kbps)\nH-高:     {}分钟 \nA-授权:    {}分钟\nR-授权刷新: {}分钟'.format(H_p3,A_p3,R_p3)
    ##hhtp4 带宽
    temp[12] = '户户通(P3/P4/P5): (可用带宽300kbps)\nH-高:   {}分钟 \nA-授权:   {}分钟\nR-授权刷新: {}分钟'.format(H_p4,A_p4,R_p4)
    ##cct 带宽
    temp[13] = '村村通: (可用带宽70kbps)\nH-高: {}分钟'.format(H_cct)
    ## hht p3 今日开卡数据
    temp[35] = '{0}00:00-{1}00:00\n创建订户: {2}\n\n{0}8:00-{1} 8:00\n创建订户: {3}\n删除订户: {4}\n\n{1}8:00 至当日巡检时间\n创建订户: {5}\n删除订户: {6}'.format(dt_y_str,\
    	dt_str,bj_sub_create_p3,utc_sub_create_m_p3,utc_sub_del_m_p3,utc_sub_create_a_p3,utc_sub_del_a_p3)
    ## hht p4 今日开卡数据
    temp[37] = '{0}00:00-{1}00:00\n创建订户: {2}\n\n{0}8:00-{1} 8:00\n创建订户: {3}\n删除订户: {4}\n\n{1}8:00至当日巡检时间\n创建订户: {5}\n删除订户: {6}'.format(dt_y_str,\
    	dt_str,bj_sub_create_p4,utc_sub_create_m_p4,utc_sub_del_m_p4,utc_sub_create_a_p4,utc_sub_del_a_p4)
    ##cct 今日开卡数据
    temp[39] = '{0}8:00-{1}8:00\n创建订户: {2}\n删除订户: {3}\n\n{1}8:00至当日巡检时间\n创建订户: {4}\n删除订户: {5}'.format(dt_y_str,\
    	dt_str,utc_sub_create_m_cct,utc_sub_del_m_cct,utc_sub_create_a_cct,utc_sub_del_a_cct)
    ##返回赋值后的星期列，周几，周一日期，周日日期，和数据日期
    return temp,week_day,monday,sunday,Date

##main code
##进入数据目录
os.chdir(DIR2)

##获取数据目录中的文件
L=os.listdir()

##过滤数据文件夹中符合条件的文件
L_week = {'monday.csv':1,'tuesday.csv':2,'wednesday.csv':3,'thurday.csv':4,'friday.csv':5,'saturday.csv':6,'sunday.csv':7}

##文件名完全过滤
L_data = [ i for i in L if i in L_week.keys()]

##如果没有发现相关文件，退出
if not L_data:
    print('Cannot find required SMS files or duplicated files,exiting...')
    exit()

##按星期排序
df_week = pd.DataFrame({'list':L_data})
df_week['order'] = df_week.list.map(L_week)
##按星期顺序排序后的文件名列表
datas = list(df_week.sort_values('order').list)


##导入日报模板
template_data = os.path.join(DIR3,'系统运行报告小结_template.xlsx')

df_daily = pd.read_excel(template_data,header=None)

for week_dat in datas:
    out_data,week_day,monday,sunday,Date = csv_report_excel(week_dat)

    ##需要取代的列表
    col_nu = df_daily.loc[:,df_daily.loc[2,:] == week_day ].columns[0]

    ##替换列
    df_daily[col_nu] = out_data



##定义写入excel的格式
#进入程序主目录
os.chdir(DIR1)

import xlsxwriter

writer = pd.ExcelWriter('系统运行报告小结_{}.xlsx'.format(Date), engine='xlsxwriter')

df_daily.to_excel(writer,sheet_name='Sheet1',index=0,header=None)

workbook  = writer.book
worksheet = writer.sheets['Sheet1']

##第一行的格式
format_header = workbook.add_format({
    'bold': True,
    'font_name': '微软雅黑',
    'valign': 'left',
 	'font_size':18,
    'border': 0})

##第二行和第三行的格式
format_header_2 = workbook.add_format({
    'bold': True,
    'font_name': '华文仿宋',
    'align':'center',
    'valign': 'vcenter',
 	'font_size':12,
    'border': 1})

##第二列和第三列的格式
format_item_name = workbook.add_format({
    'bold': False,
    'font_name': '华文仿宋',
    'align':'center',
    'valign': 'vcenter',
 	'text_wrap': True,
 	'font_size':12,
    'border': 1})

##第二列和第三列的格式
format_merge_1 = workbook.add_format({
    'border': 0})


##正文的格式
format_1 = workbook.add_format({
    'font_name': '华文仿宋',
 	'font_size':12,
 	'text_wrap': True,
    'border': 1})

##小标题行的格式
worksheet.set_row(34,None,format_header_2)
worksheet.set_row(36,None,format_header_2)
worksheet.set_row(38,None,format_header_2)


report_header ='CA系统运行报告日报   ({}-{})'.format(monday.strftime('%m.%d'),sunday.strftime('%m.%d'))

##第一列的格式(index)
worksheet.set_column('A:A',6.45,format_header_2)

worksheet.merge_range(1,0,2,0,'{}'.format(df_daily.iloc[1,0]),format_header_2)
worksheet.merge_range('A5:A6', 2, format_header_2)
worksheet.merge_range('A8:A14', 4, format_header_2)
worksheet.merge_range('A16:A34', 6, format_header_2)
worksheet.merge_range('A35:A41', 7, format_header_2)
worksheet.merge_range('A43:A44', 9, format_header_2)

##第二和第三列的格式(分项)


#单行两列的合并
double_merge_rows = [3,4,5,6,10] + list(range(14,34)) 
double_merge_rows.append(41)

for i in double_merge_rows:
	worksheet.merge_range(i,1,i,2,'{}'.format(df_daily.iloc[i,1]),format_item_name)

#不规律的合并
worksheet.merge_range(1,1,2,2,'{}'.format(df_daily.iloc[1,1]),format_item_name)
worksheet.merge_range(7,1,9,2,'{}'.format(df_daily.iloc[7,1]),format_item_name)
worksheet.merge_range(11,1,13,2,'{}'.format(df_daily.iloc[11,1]),format_item_name)
worksheet.merge_range(34,1,40,1,'{}'.format(df_daily.iloc[34,1]),format_item_name)
worksheet.merge_range(34,2,39,2,'{}'.format(df_daily.iloc[34,2]),format_item_name)
worksheet.merge_range(42,1,43,1,'{}'.format(df_daily.iloc[42,1]),format_item_name)

#个别单元格的格式
worksheet.write(40,2,'{}'.format(df_daily.iloc[40,2]),format_item_name)
worksheet.write(42,2,'{}'.format(df_daily.iloc[42,2]),format_item_name)
worksheet.write(43,2,'{}'.format(df_daily.iloc[43,2]),format_item_name)

##第一行前三列的格式合并单元格
worksheet.merge_range('A1:C1', report_header, format_header)

##星期列的列宽度和格式
worksheet.set_column('C:J', 43.73,format_1) 

##第三行的格式
worksheet.set_row(2,None,format_header_2)

##前两行的修饰合并
worksheet.merge_range('D1:J1','',format_merge_1)
worksheet.merge_range('D2:J2','',format_header_2)


##删除不用的行
worksheet.set_default_row(hide_unused_rows=True)
##删除不用的列
worksheet.set_column('K:XFD', None, None, {'hidden': True})
worksheet.freeze_panes(3,3)


writer.save()





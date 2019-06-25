#!/bin/bash
################################
##This Script is used to collect
##HHT statistic data
##By: Dan Xie
##Version: 1.02
##Date:2019.06.14
##requirement
##***data directory is required ***
##***log directory is required ***
##***week_list.txt is required ***
###############################

#########variables##########
log_date=`date +%m%d%Y`
log_yes=$(date -d "1 day ago" +%m%d%Y)
log_before_yes=$(date -d "2 day ago" +%m%d%Y)
db_date=`date +%m/%d/%Y`
db_yes=$(date -d "1 day ago" +%m/%d/%Y)
report_date=`date +%Y%m%d`
week_day=`date +%A| tr '[A-Z]' '[a-z]'`


CSS_LOG_Today="CSS_ALL_${log_date}.dat"
CSS_LOG_Yes="CSS_ALL_${log_yes}.dat"
CSS_LOG_Before_Yes="CSS_ALL_${log_before_yes}.dat" 

DIR="/opt/nds/custom_tools/utils/daily_report_gen/"

log_dir=`echo ${DIR}log`
output_dir=`echo ${DIR}data`

LOG_HHT1_DIR="/DTH_DATA/backup/HHTEMMG1/CSSLOG/"
LOG_HHT5_DIR="/DTH_DATA/backup/HHTEMMG5/CSSLOG/"

LOG_HHT1_DIR="/opt/nds/emmg/log/"

daily_data="/opt/nds/custom_tools/log/check_result/dailycheck_result_${report_date}"
daily_data_p4="/opt/nds/custom_tools/log/check_result/dailycheck_result_${report_date}_p4"

RUN=$(basename $0)
TMP1="/tmp/$RUN.1.tmp"
TMP2="/tmp/$RUN.2.tmp"
TMP3="/tmp/$RUN.3.tmp"
TMP4="/tmp/$RUN.4.tmp"
TMP5="/tmp/$RUN.5.tmp"
TMP6="/tmp/$RUN.6.tmp"
TMP7="/tmp/$RUN.7.tmp"
RUN_LOG="${log_dir}/${RUN}_${log_date}.log"
HHTEMMG1="10.146.90.91"
HHTEMMG5="10.145.90.113"
FIR1="192.168.70.99"
FIR2="10.145.90.253"

#############functions############

#card data in BJ time

bj_daily_data(){

LOG_1="${1}$2"

LOG_2="${1}$3"

if [ ! -f $LOG_1 ] || [ ! -f $LOG_2 ]
then
echo "`date +"%b %d %H:%M:%S"`: Cannot find $2 or $3 in $1, set BJ sub creation to 0" >> $RUN_LOG
echo 0
return 1
fi

TIME="16"

while true;do

	a=$(/bin/cat -n $LOG_2 | sed -n '/'${TIME}':..:../p'| head -1 | awk '{print $1}')

	if [ -z "$a" ] && [ $TIME -le 23 ];then
	  echo "`date +"%b %d %H:%M:%S"`: No data in ${TIME}:..:.., cutting data from `/usr/bin/expr $TIME + 1`:..:.. in $LOG_2" >> $RUN_LOG
	  TIME=$(($TIME + 1))
	else
	  break
	fi

done

b=$(/bin/cat -n $LOG_2 | tail -1 | awk '{print $1}')

linecut1=$(/usr/bin/expr $b - $a + 1)

TIME="16"

while true;do

	c=$(/bin/cat -n $LOG_1 | sed -n '/'${TIME}':..:../p'| head -1 | awk '{print $1}')

	if [ -z "$c" ] && [ $TIME -ge 1 ];then
	  echo "`date +"%b %d %H:%M:%S"`: No data in ${TIME}:..:.., cutting data from `/usr/bin/expr $TIME + 1`:..:.. in $LOG_1" >> $RUN_LOG
	  TIME=$(($TIME - 1))
	else
	  break
	fi

done

linecut2=$( /usr/bin/expr $c - 1 )

if [ -z $a ] && [ ! -z $c ];then
	/bin/cat $LOG_1 | head -$linecut2 > $TMP1  
elif [ -z $c ] && [ ! -z $a ];then 
	/bin/cat $LOG_2 | tail -$linecut1 > $TMP1
elif [ -z $c ] && [ -z $a ];then
	echo "`date +"%b %d %H:%M:%S"`: No related info found in $2 and $3 in $1 , BJ sub data will set to 0 " >> $RUN_LOG 
elif [ ! -z $c ] && [ ! -z $a ];then
	/bin/cat $LOG_2 | tail -$linecut1 > $TMP1
	/bin/cat $LOG_1 | head -$linecut2 >> $TMP1
fi
nu=$(less ${TMP1} | grep -i "^;0003M.\{32\}S.\{8\}1I" | grep "OOOOOO"| cut -c 50-61 | sort | uniq | wc -l)

echo $nu 

rm -rf $TMP1

}



#####main code#######

: > $TMP1
: > $TMP2
: > $TMP3
: > $TMP4
: > $TMP5

###BJ card activation
bj_p3=`bj_daily_data $LOG_HHT1_DIR $CSS_LOG_Yes $CSS_LOG_Before_Yes`

bj_p4=`bj_daily_data $LOG_HHT1_DIR $CSS_LOG_Yes $CSS_LOG_Before_Yes`

##utc card activation

utc_today_create_p3=`/usr/bin/ssh root@${HHTEMMG1} "cd /opt/nds/emmg/log;/bin/cat $CSS_LOG_Today" 2>/dev/null | grep -i "^;0003M.\{32\}S.\{8\}1I"|grep OOOOOO|cut -c 50-61|sort|uniq|wc -l`
utc_yes_create_p3=`/usr/bin/ssh root@${HHTEMMG1} "cd /opt/nds/emmg/log;/bin/cat $CSS_LOG_Yes" 2>/dev/null | grep -i "^;0003M.\{32\}S.\{8\}1I"|grep OOOOOO|cut -c 50-61|sort|uniq|wc -l`
utc_today_create_p4=`/usr/bin/ssh root@${HHTEMMG1} "cd /opt/nds/emmg/log;/bin/cat $CSS_LOG_Today" 2>/dev/null | grep -i "^;0003M.\{32\}S.\{8\}1I"|grep OOOOOO|cut -c 50-61|sort|uniq|wc -l`
utc_yes_create_p4=`/usr/bin/ssh root@${HHTEMMG1} "cd /opt/nds/emmg/log;/bin/cat $CSS_LOG_Yes" 2>/dev/null | grep -i "^;0003M.\{32\}S.\{8\}1I"|grep OOOOOO|cut -c 50-61|sort|uniq|wc -l`


##utc card deletion

utc_today_del_p3=`/usr/bin/ssh root@${HHTEMMG1} "/opt/nds/custom_tools/utils/hht_del_count.sh $db_date" 2>/dev/null`
utc_yes_del_p3=`/usr/bin/ssh root@${HHTEMMG1} "/opt/nds/custom_tools/utils/hht_del_count.sh $db_yes" 2>/dev/null`
utc_today_del_p4=`/usr/bin/ssh root@${HHTEMMG1} "/opt/nds/custom_tools/utils/hht_del_count.sh $db_date" 2>/dev/null`
utc_yes_del_p4=`/usr/bin/ssh root@${HHTEMMG1} "/opt/nds/custom_tools/utils/hht_del_count.sh $db_yes" 2>/dev/null`


##HHT statistic
/usr/bin/ssh root@${HHTEMMG1} "/bin/cat $daily_data" 2>/dev/null > $TMP2 
/usr/bin/ssh root@${HHTEMMG1} "/bin/cat $daily_data_p4" 2>/dev/null > $TMP3 

sub_create_p3=`/bin/sed -n '1p' $TMP2 | awk -F ': ' '{print$NF}'`
card_total_p3=`/bin/sed -n '2p' $TMP2 | awk -F ': ' '{print$NF}'`
sub_create_cct=`/bin/sed -n '3p' $TMP2 | awk -F ': ' '{print$NF}'`
card_total_cct=`/bin/sed -n '4p' $TMP2 | awk -F ': ' '{print$NF}'`
H_p3=`/bin/sed -n '/HHT Pri_H/p' $TMP2 | head -1 | awk -F ': ' '{print$NF}'`
A_p3=`/bin/sed -n '/HHT Pri_A/p' $TMP2 | head -1 | awk -F ': ' '{print$NF}'`
R_p3=`/bin/sed -n '/HHT Pri_R/p' $TMP2 | head -1 | awk -F ': ' '{print$NF}'`
H_cct=`/bin/sed -n '/CCT Pri_H/p' $TMP2 | head -1 | awk -F ': ' '{print$NF}'`

#check if it contains single number line,if it is, change the H_P3 number to it.
single_number=`/bin/awk -F '[|-]' '{ if(NF == 1) print$0}' $TMP2 | head -1`

if [ ! -z $single_number ];then
	H_p3=`echo $single_number`
fi



utc_yes_create_cct=`/bin/sed -n '/CCT Yesterday Created/p' $TMP2 | head -1 | awk -F ': ' '{print$NF}'`
if [ -z $utc_yes_create_cct ];then
	utc_today_create_cct=0
fi
utc_yes_del_cct=`/bin/sed -n '/CCT Yesterday Deleted/p' $TMP2 | head -1 | awk -F ': ' '{print$NF}'`
if [ -z $utc_yes_del_cct ];then
	utc_yes_del_cct=0
fi
utc_today_create_cct=`/bin/sed -n '/CCT Today Created/p' $TMP2 | head -1 | awk -F ': ' '{print$NF}'`
if [ -z $utc_today_create_cct ];then
	utc_today_create_cct=0
fi
utc_today_del_cct=`/bin/sed -n '/CCT Today Deleted/p' $TMP2 | head -1 | awk -F ': ' '{print$NF}'`
if [ -z $utc_today_del_cct ];then
	utc_today_del_cct=0
fi

sub_create_p4=`/bin/sed -n '1p' $TMP3 | awk -F ': ' '{print$NF}'`
card_total_p4=`/bin/sed -n '2p' $TMP3 | awk -F ': ' '{print$NF}'`
H_p4=`/bin/sed -n '3p' $TMP3 | awk -F ': ' '{print$NF}'`
A_p4=`/bin/sed -n '4p' $TMP3 | awk -F ': ' '{print$NF}'`
R_p4=`/bin/sed -n '5p' $TMP3 | awk -F ': ' '{print$NF}'`

##ASA connections
#/usr/bin/ssh user2@$FIR1 "show security flow session summary" 2>/dev/null | grep "^Sessions-in-use" | awk '{print$NF}' > $TMP4

#/usr/bin/ssh user2@$FIR2 "show security flow session summary" 2>/dev/null | grep "^Sessions-in-use" | awk '{print$NF}' >> $TMP4

echo -e "21321\n32321" > $TMP4

n=0
for i in `/bin/cat $TMP4`
do
n="`/usr/bin/expr $n + $i`"
done

asa_con=`echo $n`




echo "name,p1/p3,p4,cct" >> $TMP5
echo "sub_create,$sub_create_p3,$sub_create_p4,$sub_create_cct" >> $TMP5
echo "card_total,$card_total_p3,$card_total_p4,$card_total_cct" >> $TMP5
echo "H,$H_p3,$H_p4,$H_cct" >> $TMP5
echo "A,$A_p3,$A_p4" >> $TMP5
echo "R,$R_p3,$R_p4" >> $TMP5
echo "bj_sub_create,$bj_p3,$bj_p4" >> $TMP5
echo "utc_sub_create_m,$utc_yes_create_p3,$utc_yes_create_p4,$utc_yes_create_cct" >> $TMP5
echo "utc_sub_del_m,$utc_yes_del_p3,$utc_yes_del_p4,$utc_yes_del_cct" >> $TMP5
echo "utc_sub_create_a,$utc_today_create_p3,$utc_today_create_p4,$utc_today_del_cct" >> $TMP5
echo "utc_sub_del_a,$utc_today_del_p3,$utc_today_del_p4,$utc_today_del_cct" >> $TMP5
echo "asa,$asa_con" >> $TMP5
echo "Date,$report_date" >> $TMP5


output_file=`echo ${output_dir}/${week_day}.csv`

/bin/cat $TMP5 > $output_file

##cd to data dir
cd $output_dir

##delete unused data
weight=0

while read line;do
	if [ $weight -eq 1 ];then
		file=`echo ${line}.csv`
		if [ -f $file ];then
			rm -rf $file
		fi
	fi

	if [ $week_day == $line ];then
		weight="`/usr/bin/expr $weight + 1`"
	fi
	
done < ./week_list.txt 

#rm -rf $TMP2
#rm -rf $TMP3
#rm -rf $TMP4
#rm -rf $TMP5




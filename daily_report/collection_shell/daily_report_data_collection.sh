#!/bin/bash
################################
##This Script is used to collect
##HHT statistic data
##By: Dan Xie
##Version: 1.01
##Date:2019.06.11
##requirement
##***data directory is required ***
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


output_dir=`echo $(pwd)/data`

LOG_HHT1_DIR="/DTH_DATA/backup/HHTEMMG1/CSSLOG/"
LOG_HHT5_DIR="/DTH_DATA/backup/HHTEMMG5/CSSLOG/"

daily_data="/opt/nds/custom_tools/log/check_result/dailycheck_result_${report_date}"

RUN=$(basename $0)
TMP1="/tmp/$RUN.1.tmp"
TMP2="/tmp/$RUN.2.tmp"
TMP3="/tmp/$RUN.3.tmp"
TMP4="/tmp/$RUN.4.tmp"
TMP5="/tmp/$RUN.5.tmp"
TMP6="/tmp/$RUN.6.tmp"
TMP7="/tmp/$RUN.7.tmp"
HHTEMMG1="10.145.90.203"
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
echo 
echo "Cannot find $2 or $3 in $1 !!!"
exit 1
fi

TIME="16"

while true;do

	a=$(cat -n $LOG_2 | sed -n '/'${TIME}':..:../p'| head -1 | awk '{print $1}')

	if [ -z "$a" ];then
	  echo "No data in ${TIME}:..:.., cutting data from `expr $TIME1 + 1`:..:.. in $LOG_2"
	  TIME1=$(($TIME + 1))
	else
	  break
	fi

done

b=$(cat -n $LOG_2 | tail -1 | awk '{print $1}')

linecut1=$( expr $b - $a + 1 )

TIME="16"

while true;do

	a=$(cat -n $LOG_1 | sed -n '/'${TIME}':..:../p'| head -1 | awk '{print $1}')

	if [ -z "$a" ];then
	  echo "No data in ${TIME}:..:.., cutting data from `expr $TIME1 + 1`:..:.. in $LOG_1"
	  TIME1=$(($TIME - 1))
	else
	  break
	fi

done

linecut2=$( expr $a - 1 )

cat $LOG_2 | tail -$linecut1 > $TMP1

cat $LOG_1 | head -$linecut2 >> $TMP1

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
bj_p4=`bj_daily_data $LOG_HHT5_DIR $CSS_LOG_Yes $CSS_LOG_Before_Yes`


##utc card activation

utc_today_create_p3=`ssh root@${HHTEMMG1} "cd /opt/nds/emmg/log;cat $CSS_LOG_Today" 2>/dev/null | grep -i "^;0003M.\{32\}S.\{8\}1I"|grep OOOOOO|cut -c 50-61|sort|uniq|wc -l`
utc_yes_create_p3=`ssh root@${HHTEMMG1} "cd /opt/nds/emmg/log;cat $CSS_LOG_Yes" 2>/dev/null | grep -i "^;0003M.\{32\}S.\{8\}1I"|grep OOOOOO|cut -c 50-61|sort|uniq|wc -l`
utc_today_create_p4=`ssh root@${HHTEMMG5} "cd /opt/nds/emmg/log;cat $CSS_LOG_Today" 2>/dev/null | grep -i "^;0003M.\{32\}S.\{8\}1I"|grep OOOOOO|cut -c 50-61|sort|uniq|wc -l`
utc_yes_create_p4=`ssh root@${HHTEMMG5} "cd /opt/nds/emmg/log;cat $CSS_LOG_Yes" 2>/dev/null | grep -i "^;0003M.\{32\}S.\{8\}1I"|grep OOOOOO|cut -c 50-61|sort|uniq|wc -l`


##utc card deletion

utc_today_del_p3=`ssh root@${HHTEMMG1} "/opt/nds/custom_tools/utils/hht_del_count.sh $db_date" 2>/dev/null`
utc_yes_del_p3=`ssh root@${HHTEMMG1} "/opt/nds/custom_tools/utils/hht_del_count.sh $db_yes" 2>/dev/null`
utc_today_del_p4=`ssh root@${HHTEMMG5} "/opt/nds/custom_tools/utils/hht_del_count.sh $db_date" 2>/dev/null`
utc_yes_del_p4=`ssh root@${HHTEMMG5} "/opt/nds/custom_tools/utils/hht_del_count.sh $db_yes" 2>/dev/null`


##HHT statistic
ssh root@${HHTEMMG1} "cat $daily_data" 2>/dev/null > $TMP2 
ssh root@${HHTEMMG5} "cat $daily_data" 2>/dev/null > $TMP3 

sub_create_p3=`sed -n '1p' $TMP2 | awk -F ': ' '{print$NF}'`
card_total_p3=`sed -n '2p' $TMP2 | awk -F ': ' '{print$NF}'`
sub_create_cct=`sed -n '3p' $TMP2 | awk -F ': ' '{print$NF}'`
card_total_cct=`sed -n '4p' $TMP2 | awk -F ': ' '{print$NF}'`
H_p3=`sed -n '6p' $TMP2 | awk -F ': ' '{print$NF}'`
A_p3=`sed -n '7p' $TMP2 | awk -F ': ' '{print$NF}'`
R_p3=`sed -n '8p' $TMP2 | awk -F ': ' '{print$NF}'`
H_cct=`sed -n '9p' $TMP2 | awk -F ': ' '{print$NF}'`

utc_yes_create_cct=`sed -n '14p' $TMP2 | awk -F ': ' '{print$NF}'`
if [ -z $utc_yes_create_cct ];then
	utc_today_create_cct=0
fi
utc_yes_del_cct=`sed -n '15p' $TMP2 | awk -F ': ' '{print$NF}'`
if [ -z $utc_yes_del_cct ];then
	utc_yes_del_cct=0
fi
utc_today_create_cct=`sed -n '16p' $TMP2 | awk -F ': ' '{print$NF}'`
if [ -z $utc_today_create_cct ];then
	utc_today_create_cct=0
fi
utc_today_del_cct=`sed -n '17p' $TMP2 | awk -F ': ' '{print$NF}'`
if [ -z $utc_today_del_cct ];then
	utc_today_del_cct=0
fi

sub_create_p4=`sed -n '1p' $TMP3 | awk -F ': ' '{print$NF}'`
card_total_p4=`sed -n '2p' $TMP3 | awk -F ': ' '{print$NF}'`
H_p4=`sed -n '3p' $TMP3 | awk -F ': ' '{print$NF}'`
A_p4=`sed -n '4p' $TMP3 | awk -F ': ' '{print$NF}'`
R_p4=`sed -n '5p' $TMP3 | awk -F ': ' '{print$NF}'`

##ASA connections
ssh user2@$FIR1 "show security flow session summary" 2>/dev/null | grep "^Sessions-in-use" | awk '{print$NF}' > $TMP4

ssh user2@$FIR2 "show security flow session summary" 2>/dev/null | grep "^Sessions-in-use" | awk '{print$NF}' >> $TMP4

n=0
for i in `cat $TMP4`
do
n="`expr $n + $i`"
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

cat $TMP5 > $output_file

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
		weight="`expr $weight + 1`"
	fi
	
done < ./week_list.txt 

#rm -rf $TMP2
#rm -rf $TMP3
#rm -rf $TMP4
#rm -rf $TMP5




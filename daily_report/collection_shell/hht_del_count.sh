#!/bin/bash


DATE=`date  +%m/%d/%Y`
DATE_Yes=`date -d last-day +%m/%d/%Y`

. /opt/nds/emmg/utils/camcenv.sh;
. /opt/oracle/EMMG.env;

NU=`sqlplus -S "supervis/SuperviS123!@EMMG" << !
set heading off
set feedback off
set pagesize 0
set verify off
set echo off
select count (*) from DEL_SUB t where trunc(DELDATE) = TO_DATE('$1', 'MM/DD/YYYY');
exit
!`

echo $NU

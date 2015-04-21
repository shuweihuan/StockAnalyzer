#!/usr/bin/bash

source ../conf/global.conf

################################
########### Get Data ###########
################################

cd $SRC_PATH/spider
python get_fund_data.py $RAW_PATH
cd - > /dev/null


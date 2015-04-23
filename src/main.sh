#!/usr/bin/bash

source ../conf/global.conf

################################
######### Environment ##########
################################

if [ -z $RAW_PATH ]; then
	mkdir $RAW_PATH
fi

if [ -z $DATA_PATH ]; then
	mkdir $DATA_PATH
fi

################################
########### Get Data ###########
################################

cd $SRC_PATH/spider
python get_fund_data.py $RAW_PATH
cd - > /dev/null

################################
########## Merge Data ##########
################################

cd $SRC_PATH/analyzer
python merge_data.py $RAW_PATH $DATA_PATH
cd - > /dev/null

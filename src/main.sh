#!/usr/bin/bash

source ../conf/global.conf

################################
######### Environment ##########
################################

if [ -z $DATA_PATH ]; then
	mkdir $DATA_PATH
fi

################################
########### Get Data ###########
################################

cd $SRC_PATH/spider
python get_fund_data.py
cd - > /dev/null

cd $SRC_PATH/spider
python get_stock_data.py
cd - > /dev/null

#################################
######### Analyze Data ##########
#################################

cd $SRC_PATH/analyzer
python fund_stock_position.py
cd - > /dev/null

#################################
########### Strategy ############
#################################

cd $SRC_PATH/strategy

cd - > /dev/null


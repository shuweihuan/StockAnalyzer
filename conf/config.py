#!/usr/bin/python
#coding: utf-8

import os

MAIN_PATH = "/root/workspace/StockAnalyzer"

SRC_PATH = os.path.join(MAIN_PATH, "src")
CONF_PATH = os.path.join(MAIN_PATH, "conf")
DATA_PATH = os.path.join(MAIN_PATH, "data")
ANALYSIS_PATH = os.path.join(MAIN_PATH, "analysis")

STOCK_LIST_DATA_PATH = os.path.join(DATA_PATH, "stock_list.csv")
STOCK_HISTORY_PATH = os.path.join(DATA_PATH, "stock_history")
FUND_INFO_DATA_PATH = os.path.join(DATA_PATH, "fund_info.csv")
FUND_TOP_STOCK_PATH = os.path.join(DATA_PATH, "fund_top_stock")

FUND_STOCK_POSITION_PATH = os.path.join(ANALYSIS_PATH, "fund_stock_position")

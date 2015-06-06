#!/usr/bin/python
#coding: utf-8

import os
import pandas as pd

# path setting

MAIN_PATH = "/root/workspace/StockAnalyzer"

SRC_PATH = os.path.join(MAIN_PATH, "src")
CONF_PATH = os.path.join(MAIN_PATH, "conf")
DATA_PATH = os.path.join(MAIN_PATH, "data")
ANALYSIS_PATH = os.path.join(MAIN_PATH, "analysis")

STOCK_HISTORY_PATH = os.path.join(DATA_PATH, "stock_history")
INDEX_HISTORY_PATH = os.path.join(DATA_PATH, "index_history")
STOCK_REPORT_PATH = os.path.join(DATA_PATH, "stock_report")
STOCK_PROFIT_PATH = os.path.join(DATA_PATH, "stock_profit")
STOCK_GROWTH_PATH = os.path.join(DATA_PATH, "stock_growth")
STOCK_DEBT_PATH = os.path.join(DATA_PATH, "stock_debt")
STOCK_CASH_PATH = os.path.join(DATA_PATH, "stock_cash")
FUND_TOP_STOCK_PATH = os.path.join(DATA_PATH, "fund_top_stock")

STOCK_LIST_DATA_PATH = os.path.join(DATA_PATH, "stock_list.csv")
STOCK_DATA_PATH = os.path.join(DATA_PATH, "stock_data.csv")
INDEX_DATA_PATH = os.path.join(DATA_PATH, "index_data.csv")
STOCK_BASICS_DATA_PATH = os.path.join(DATA_PATH, "stock_basics.csv")
FUND_INFO_DATA_PATH = os.path.join(DATA_PATH, "fund_info.csv")

FUND_STOCK_POSITION_PATH = os.path.join(ANALYSIS_PATH, "fund_stock_position")


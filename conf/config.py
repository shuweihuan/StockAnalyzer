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

INDEX_HISTORY_PATH = os.path.join(DATA_PATH, "index_history")
STOCK_HISTORY_PATH = os.path.join(DATA_PATH, "stock_history")
STOCK_RESTORATION_HISTORY_PATH = os.path.join(DATA_PATH, "stock_restoration_history")
STOCK_REPORT_PATH = os.path.join(DATA_PATH, "stock_report")
STOCK_PROFIT_PATH = os.path.join(DATA_PATH, "stock_profit")
STOCK_GROWTH_PATH = os.path.join(DATA_PATH, "stock_growth")
STOCK_DEBTPAYING_PATH = os.path.join(DATA_PATH, "stock_debtpaying")
STOCK_CASHFLOW_PATH = os.path.join(DATA_PATH, "stock_cashflow")
STOCK_FUNDHOLDING_PATH = os.path.join(DATA_PATH, "stock_fundholding")
STOCK_FORECAST_PATH = os.path.join(DATA_PATH, "stock_forecast")
FUND_TOP_STOCK_PATH = os.path.join(DATA_PATH, "fund_top_stock")

INDEX_PRICE_DATA_PATH = os.path.join(DATA_PATH, "index_price.csv")
STOCK_PRICE_DATA_PATH = os.path.join(DATA_PATH, "stock_price.csv")
STOCK_BASICS_DATA_PATH = os.path.join(DATA_PATH, "stock_basics.csv")
FUND_INFO_DATA_PATH = os.path.join(DATA_PATH, "fund_info.csv")

FUND_STOCK_POSITION_PATH = os.path.join(ANALYSIS_PATH, "fund_stock_position")
STOCK_DAILY_INCR_PATH = os.path.join(ANALYSIS_PATH, "stock_daily_incr")
STOCK_DAILY_INCR_DATA_PATH = os.path.join(ANALYSIS_PATH, "stock_daily_incr.csv")
STOCK_QUARTERLY_INCR_DATA_PATH = os.path.join(ANALYSIS_PATH, "stock_quarterly_incr.csv")


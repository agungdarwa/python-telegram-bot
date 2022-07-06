#!pip install tradingview_ta workerpool colorama

from colorama import Fore, Style
from tradingview_ta import TA_Handler, Interval, get_multiple_analysis
import json
import tradingview_ta, requests, argparse
import time
import workerpool

import multiprocessing
from multiprocessing import Pool, TimeoutError
import os

thread = multiprocessing.cpu_count()

data_list = []

# arg_parser = argparse.ArgumentParser()

# arg_parser.add_argument("--proxy", help="Use HTTP proxy")
# arg_parser.add_argument("--secureproxy", help="Use HTTPS proxy")

# args = arg_parser.parse_args()

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def scanner(screener,exchange,symbol,interval):
    # proxies = {}
    # if args.proxy:
    #     proxies["http"] = args.proxy
    # if args.secureproxy:
    #     proxies["https"] = args.secureproxy

    handler = TA_Handler(
        symbol=symbol,
        interval=interval,
        screener=screener,
        exchange=exchange,
        # proxies = proxies
    )
    try:
        return handler.get_indicators()
    except Exception as e:
        return e


def runner(data):
    # for i in data:
    symbol = data[0]
    tf = data[1]
    screener="crypto"
    exchange="binance"
    if tf == "1m":
        interval=Interval.INTERVAL_1_MINUTE
    elif tf == "5m":
        interval=Interval.INTERVAL_5_MINUTES
    elif tf == "15m":
        interval=Interval.INTERVAL_15_MINUTES   
    elif tf == "30m":
        interval=Interval.INTERVAL_30_MINUTES
    elif tf == "1h":
        interval=Interval.INTERVAL_1_HOUR
    elif tf == "2h":
        interval=Interval.INTERVAL_2_HOURS
    elif tf == "4h":
        interval=Interval.INTERVAL_4_HOURS
    elif tf == "1d":
        interval=Interval.INTERVAL_1_DAY
    elif tf == "1w":
        interval=Interval.INTERVAL_1_WEEK
    elif tf == "1M":
        interval=Interval.INTERVAL_1_MONTH

    datas = scanner(screener,exchange,symbol,interval)
    datas.update({"screener":screener,"exchange":exchange,"symbol":symbol,"interval":tf})
    # data_list.append(datas)
    print(datas)

all_symbol = ["1000LUNC/BUSD", "1000SHIB/USDT", "1000XEC/USDT", "1INCH/USDT", "AAVE/USDT", "ADA/BUSD", "ADA/USDT", "ALGO/USDT", "ALICE/USDT", "ALPHA/USDT", "ANC/BUSD", "ANKR/USDT", "ANT/USDT", "APE/BUSD", "APE/USDT", "API3/USDT", "AR/USDT", "ARPA/USDT", "ATA/USDT", "ATOM/USDT", "AUDIO/USDT", "AVAX/BUSD", "AVAX/USDT", "AXS/USDT", "BAKE/USDT", "BAL/USDT", "BAND/USDT", "BAT/USDT", "BCH/USDT", "BEL/USDT", "BLZ/USDT", "BNB/BUSD", "BNB/USDT", "BNX/USDT", "BTC/BUSD", "BTC/USDT", "BTCDOM/USDT", "BTS/USDT", "C98/USDT", "CELO/USDT", "CELR/USDT", "CHR/USDT", "CHZ/USDT", "COMP/USDT", "COTI/USDT", "CRV/USDT", "CTK/USDT", "CTSI/USDT", "CVC/USDT", "DAR/USDT", "DASH/USDT", "DEFI/USDT", "DENT/USDT", "DGB/USDT", "DODO/BUSD", "DOGE/BUSD", "DOGE/USDT", "DOT/BUSD", "DOT/USDT", "DUSK/USDT", "DYDX/USDT", "EGLD/USDT", "ENJ/USDT", "ENS/USDT", "EOS/USDT", "ETC/USDT", "ETH/BUSD", "ETH/USDT", "FIL/USDT", "FLM/USDT", "FLOW/USDT", "FTM/BUSD", "FTM/USDT", "FTT/BUSD", "FTT/USDT", "GAL/BUSD", "GAL/USDT", "GALA/BUSD", "GALA/USDT", "GMT/BUSD", "GMT/USDT", "GRT/USDT", "GTC/USDT", "HBAR/USDT", "HNT/USDT", "HOT/USDT", "ICP/BUSD", "ICP/USDT", "ICX/USDT", "IMX/USDT", "IOST/USDT", "IOTA/USDT", "IOTX/USDT", "JASMY/USDT", "KAVA/USDT", "KLAY/USDT", "KNC/USDT", "KSM/USDT", "LINA/USDT", "LINK/BUSD", "LINK/USDT", "LIT/USDT", "LPT/USDT", "LRC/USDT", "LTC/USDT", "LUNA2/BUSD", "MANA/USDT", "MASK/USDT", "MATIC/USDT", "MKR/USDT", "MTL/USDT", "NEAR/BUSD", "NEAR/USDT", "NEO/USDT", "NKN/USDT", "OCEAN/USDT", "OGN/USDT", "OMG/USDT", "ONE/USDT", "ONT/USDT", "OP/USDT", "PEOPLE/USDT", "QTUM/USDT", "RAY/USDT", "REEF/USDT", "REN/USDT", "RLC/USDT", "ROSE/USDT", "RSR/USDT", "RUNE/USDT", "RVN/USDT", "SAND/USDT", "SC/USDT", "SFP/USDT", "SKL/USDT", "SNX/USDT", "SOL/BUSD", "SOL/USDT", "SRM/USDT", "STMX/USDT", "STORJ/USDT", "SUSHI/USDT", "SXP/USDT", "THETA/USDT", "TLM/BUSD", "TLM/USDT", "TOMO/USDT", "TRB/USDT", "TRX/BUSD", "TRX/USDT", "UNFI/USDT", "UNI/USDT", "VET/USDT", "WAVES/BUSD", "WAVES/USDT", "WOO/USDT", "XEM/USDT", "XLM/USDT", "XMR/USDT", "XRP/BUSD", "XRP/USDT", "XTZ/USDT", "YFI/USDT", "ZEC/USDT", "ZEN/USDT", "ZIL/USDT", "ZRX/USDT"]
timeframes = {'1m','5m','15m','30m','1h','2h','4h','1d','1w','1M'}

inout = []

for i in all_symbol:
    for x in timeframes:
        symbol = i.replace("/","")+"PERP"
        inout.append([symbol,x]) 

# pool = workerpool.WorkerPool(size=thread)
# pool.map(runner,inout)
# pool.shutdown()
# pool.wait()
if __name__ == '__main__':
    tic = time.perf_counter()
    # start 4 worker processes
    # with Pool(processes=thread) as pool:
        # pool.map(runner, inout)
    pool = workerpool.WorkerPool(size=thread)
    pool.map(runner,inout)
    pool.shutdown()
    pool.wait()
    toc = time.perf_counter()
    print(f"Downloaded analysis in {toc - tic:0.4f} seconds")

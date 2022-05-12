from myModule import sqlCmd,myIO
import stockInfo
import config
import pandas as pd

Q=myIO.loadVar(config.getQMatPath())
print(config.getQMatPath())
print(len(Q))
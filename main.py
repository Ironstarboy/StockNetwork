import returnMat
import timeSeries
import Q5min
import mat2G
import plotQ
import config
from myModule import myIO

returnMat.getReturnMat(config.get('mkt'))
timeSeries.fileterNotStaionaryStock()
Q5min.run()
mat2G.mat2edge(myIO.loadVar(config.getQMatPath()))
plotQ.plotQ()
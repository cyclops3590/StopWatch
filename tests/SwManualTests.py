# coding=utf-8
"""
Output should look similar to the following:

Summary for StopWatch Default stop watch
==========================================================================================
default: Duration: 1.003455 seconds in 1 lap(s)
Clock One: Duration: 1.004869 seconds in 1 lap(s)
Clock Three: Duration: 0.000005 seconds in 1 lap(s)
------------------------------------------------------------------------------------------
1 Hidden Clock(s): 2.008688 seconds in 1 lap(s)
==========================================================================================
Total Duration: 4.017017 seconds
"""
from pyStopWatch.StopWatch import StopWatch
import time

sw = StopWatch()

sw.addclock('clock1','Clock One')
sw.addclock('clock2','Clock Two',False)
sw.addclock('clock3','Clock Three')

sw.start()
time.sleep(1)
sw.stop()
sw.start('clock1')
sw.start('clock2')
time.sleep(1)
sw.stop('clock1')
time.sleep(1)
sw.stop('clock2')
sw.start('clock3')
sw.stop('clock3')

print(sw.summary)

#!/usr/bin/env python
# coding=utf-8
"""
StopWatch Test Definitions
"""
import unittest2
from StopWatch.StopWatch import StopWatch
from StopWatch.StopWatchException import StopWatchException
import time


class StopWatchTester(unittest2.TestCase):
    def setUp(self):
        self.stopwatch = StopWatch()

    def testSingleClock(self):
        # deals with default clock only so clock name is not to be given

        # test trying to stop an an unstarted clock
        self.assertRaises(StopWatchException, self.stopwatch.stop)

        # test starting
        self.stopwatch.start()
        self.assertTrue(self.stopwatch.isstarted(), 'Clock not showing started')

        # test starting already started clock
        self.assertRaises(StopWatchException, self.stopwatch.start)

        # test stopping clock
        self.stopwatch.stop()
        self.assertTrue(self.stopwatch.isstopped(), 'Clock is apparently running')

        # test lapcount
        self.assertEqual(1, self.stopwatch.clocklapcount(),
                         'Clock not showing 1 lap, showing %s' % self.stopwatch.clocklapcount())

        # test everused
        self.assertTrue(self.stopwatch.everused(), 'Clock not showing used')

        # test total time
        self.stopwatch.start()
        time.sleep(1)
        self.stopwatch.stop()
        self.assertGreater(self.stopwatch.clocktotalsecs(), 0, 'Clock has zero time being ran')

        # test reset
        self.stopwatch.reset()
        self.assertFalse(self.stopwatch.everused(), 'Clock shows being used after reset')


if __name__ == '__main__':
    unittest2.main()

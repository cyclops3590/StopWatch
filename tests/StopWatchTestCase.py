#!/usr/bin/env python
# coding=utf-8
"""
StopWatch Test Definitions
"""
import unittest
from pyStopWatch.StopWatch import StopWatch
from pyStopWatch.StopWatchException import StopWatchException
import time


class StopWatchTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.stopwatch = StopWatch(_recordlapdetail=True)

    def setUp(self):
        self.stopwatch.reinitialize()


    def test_Pause(self):
        self.stopwatch.start()
        time.sleep(1)
        self.stopwatch.pause()
        time.sleep(1)
        self.stopwatch.unpause()
        time.sleep(1)
        self.stopwatch.pause()
        time.sleep(1)
        self.stopwatch.unpause()
        time.sleep(1)
        self.stopwatch.pause()
        time.sleep(1)
        self.stopwatch.stop()
        print(self.stopwatch.get_clock_detail())
        self.assertEqual(int(self.stopwatch.clocktotalsecs()),3,'Incorrect total time: {0}'.format(self.stopwatch.clocktotalsecs()))


    def test_LapDetail(self):
        self.stopwatch.start()
        time.sleep(1)
        self.stopwatch.stop()
        time.sleep(1)
        self.stopwatch.start()
        time.sleep(1)
        self.stopwatch.pause()
        time.sleep(1)
        self.stopwatch.unpause()
        time.sleep(1)
        self.stopwatch.pause()
        time.sleep(1)
        self.stopwatch.stop()
        self.assertEqual(int(self.stopwatch.clocktotalsecs()),3,'Incorrect total time: {0}'.format(self.stopwatch.clocktotalsecs()))
        self.assertEqual(int(self.stopwatch.lapdetail(1)['total']), 1, 'Incorrect lap 1 time: {0}'.format(self.stopwatch.lapdetail(1)['total']))
        self.assertEqual(int(self.stopwatch.lapdetail(2)['total']), 2, 'Incorrect lap 2 time: {0}'.format(self.stopwatch.lapdetail(1)['total']))
        self.assertRaises(StopWatchException,self.stopwatch.lapdetail,3)


    def test_SingleClock(self):
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

    def test_MultiClock(self):
        # deals with testing 2 clocks in addition to the default clock

        # testing adding new clock
        self.assertEqual(len(self.stopwatch.availableclocks()), 1, 'Incorrect available clock count, should be 1.')
        self.stopwatch.addclock('newclock1', 'New Clock 1')
        self.assertEqual(len(self.stopwatch.availableclocks()), 2, 'Incorrect available clock count, should be 2.')
        self.stopwatch.addclock('newclock2', 'New Clock 2')
        self.assertEqual(len(self.stopwatch.availableclocks()), 3, 'Incorrect available clock count, should be 3.')

        # testing used clocks
        self.assertEqual(len(self.stopwatch.startedclocks()), 0, 'Incorrect started clock count, should be 0.')
        self.stopwatch.start('newclock1')
        self.assertEqual(len(self.stopwatch.startedclocks()), 1, 'Incorrect started clock count, should be 1.')
        self.stopwatch.start('default')
        self.assertEqual(len(self.stopwatch.startedclocks()), 2, 'Incorrect started clock count, should be 2.')
        self.assertEqual(len(self.stopwatch.stoppedclocks()), 1, 'Incorrect stopped clock count, should be 1.')
        self.stopwatch.stopall()
        self.assertEqual(len(self.stopwatch.startedclocks()), 0, 'Incorrect started clock count, should be 0.')
        self.assertEqual(len(self.stopwatch.usedclocks()), 2, 'Incorrect used clock count, should be 2.')
        self.stopwatch.start('newclock1')
        self.assertEqual(len(self.stopwatch.stoppedclocks()), 2, 'Incorrect stopped clock count, should be 2.')
        self.stopwatch.stop('newclock1')
        self.assertEqual(self.stopwatch.clocklapcount('newclock1'), 2, 'Incorrect clock lapcount, should be 2.')
        self.stopwatch.reset('newclock1')
        self.assertEqual(self.stopwatch.clocklapcount('newclock1'), 0, 'Incorrect clock lapcount, should be 0.')
        self.assertEqual(len(self.stopwatch.usedclocks()), 1, 'Incorrect used clock count, should be 1.')
        self.stopwatch.resetall()
        self.assertEqual(len(self.stopwatch.usedclocks()), 0, 'Incorrect used clock count, should be 0.')
        self.assertEqual(len(self.stopwatch.availableclocks()), 3, 'Incorrect available clock count, should be 3.')

        # testing removing clocks
        self.stopwatch.removeclock('newclock2')
        self.assertEqual(len(self.stopwatch.availableclocks()), 2, 'Incorrect available clock count, should be 2.')
        self.stopwatch.reinitialize()
        self.assertEqual(len(self.stopwatch.availableclocks()), 1, 'Incorrect available clock count, should be 1.')

        self.assertRaises(StopWatchException, self.stopwatch.removeclock, 'bogus')

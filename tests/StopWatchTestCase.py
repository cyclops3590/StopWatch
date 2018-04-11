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


    def __run_clocks(self,multi=False,with_hidden=False):
        """
        Runs clocks depending on which ones are desired for test
        :param multi:
        :param with_hidden:
        :return:
        """
        if multi:
            self.stopwatch.addclock('clock2', 'Clock 2')
        if with_hidden:
            self.stopwatch.addclock('clock3', 'Hidden Clock', False)

        # Lap 1
        self.stopwatch.start()
        if multi: self.stopwatch.start('clock2')
        if with_hidden: self.stopwatch.start('clock3')
        time.sleep(1)
        self.stopwatch.stop()
        if multi: self.stopwatch.stop('clock2')
        if with_hidden: self.stopwatch.stop('clock3')

        # Lap 2
        self.stopwatch.start()
        if multi: self.stopwatch.start('clock2')
        if with_hidden: self.stopwatch.start('clock3')
        time.sleep(1)
        self.stopwatch.pause()
        if multi: self.stopwatch.pause('clock2')
        time.sleep(1)
        self.stopwatch.unpause()
        if multi: self.stopwatch.unpause('clock2')
        time.sleep(1)
        self.stopwatch.pause()
        if multi: self.stopwatch.pause('clock2')
        if with_hidden: self.stopwatch.pause('clock3')
        time.sleep(1)
        self.stopwatch.unpause()
        if multi: self.stopwatch.unpause('clock2')
        time.sleep(1)
        self.stopwatch.pause()
        time.sleep(1)
        self.stopwatch.stop()
        if multi: self.stopwatch.stop('clock2')
        if with_hidden: self.stopwatch.stop('clock3')

    def test_Pause(self):
        self.__run_clocks()
        self.assertEqual(int(self.stopwatch.clocktotalsecs()),4,'Incorrect total time: {0}'.format(self.stopwatch.clocktotalsecs()))


    def test_LapDetail(self):
        self.__run_clocks()
        self.assertEqual(int(self.stopwatch.clocktotalsecs()),4,'Incorrect total time: {0}'.format(int(self.stopwatch.clocktotalsecs())))
        self.assertEqual(int(self.stopwatch.lapdetail(1)['total']), 1, 'Incorrect lap 1 time: {0}'.format(self.stopwatch.lapdetail(1)['total']))
        self.assertEqual(int(self.stopwatch.lapdetail(2)['total']), 3, 'Incorrect lap 2 time: {0}'.format(self.stopwatch.lapdetail(2)['total']))
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


    def test_DefaultIsOverall(self):
        self.__run_clocks(multi=True)
        summary = self.stopwatch.get_summary(json=True,default_is_overall=True)
        self.assertEqual(self.stopwatch.clocktotalsecs('default'),summary['Overall']['total'],'Overall does not match default')
        self.assertEqual(self.stopwatch.clocktotalsecs('default')+self.stopwatch.clocktotalsecs('clock2'), summary['Combined']['total'],'Combined does not match default + clock2')

    def test_DefaultIsNotOverall(self):
        self.__run_clocks(multi=True)
        summary = self.stopwatch.get_summary(json=True,default_is_overall=False)
        self.assertEqual(self.stopwatch.clocktotalsecs('default')+self.stopwatch.clocktotalsecs('clock2'),summary['Overall']['total'],'Overall does not match default + clock2')
        self.assertEqual(self.stopwatch.clocktotalsecs('default')+self.stopwatch.clocktotalsecs('clock2'), summary['Combined']['total'],'Combined does not match default + clock2')

    def test_Hidden(self):
        self.__run_clocks(with_hidden=True)
        summary = self.stopwatch.get_summary(json=True)
        self.assertEqual(self.stopwatch.clocktotalsecs('default')+summary['Hidden']['total'],summary['Combined']['total'], 'Combined does not match default + hidden')


    def test_AlreadyStartedException(self):
        self.stopwatch.start()

        self.assertRaises(StopWatchException, self.stopwatch.start)

    def test_StartWhilePausedException(self):
        self.stopwatch.start()
        self.stopwatch.pause()
        self.assertRaises(StopWatchException, self.stopwatch.start)

    def test_AlreadyStoppedException(self):
        self.assertRaises(StopWatchException, self.stopwatch.stop)

    def test_AlreadyPausedException(self):
        self.stopwatch.start()
        self.stopwatch.pause()
        self.assertRaises(StopWatchException, self.stopwatch.pause)

    def test_AlreadyUnpausedException(self):
        self.stopwatch.start()
        self.assertRaises(StopWatchException, self.stopwatch.unpause)

    def test_LapcountWhileStarted(self):
        self.__run_clocks()
        self.stopwatch.start()
        time.sleep(1)
        expected = 3
        got = self.stopwatch.clocklapcount()
        self.assertEqual(expected, got, 'Incorrect lap count')

        expected = 5
        got = int(self.stopwatch.clocktotalsecs())
        self.assertEqual(expected, got, 'Incorrect clock total')

    def test_StartAll(self):
        self.__run_clocks(multi=True)
        self.assertEqual(0,len(self.stopwatch.startedclocks()), 'Incorrect number of clocks running')

        self.stopwatch.startall()
        self.assertEqual(len(self.stopwatch.availableclocks()),len(self.stopwatch.startedclocks()), 'Incorrect number of clocks running')

    def test_PauseAll(self):
        self.stopwatch.start()
        self.stopwatch.pause()
        self.assertEqual(1, len(self.stopwatch.pausedclocks()))

    def test_HasLapDetail(self):
        self.stopwatch.start()
        self.stopwatch.stop()
        self.assertTrue(self.stopwatch.haslapdetail())

    def test_NoLapDetail(self):
        self.stopwatch = StopWatch()
        self.stopwatch.start()
        self.stopwatch.stop()
        self.assertRaises(StopWatchException, self.stopwatch.lapdetail, 1)
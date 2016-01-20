# coding=utf-8
"""
This class simplifies the interactions needed to determine the time code chunks take to operate.
"""

import time
from StopWatchException import StopWatchException


class StopWatch(object):
    """
    Class definition for StopWatch which is a class to simply perform start, stop and print duration strings.
    This takes care of slightly redundant and more complex logic to provide an easy interface for
    stopwatch functionality
    """

    def __init__(self, _swtitle='StopWatch Default'):
        """
        initialize StopWatch object instance
        :param _swtitle: Title for the stop watch
        :type _swtitle: str
        :var self._clocks: various clocks being tracked.  'default' is only one setup immediately
        :type self._clocks: dict
        :return: n/a
        """
        self.title = _swtitle
        self._clocks = {
            'default': {
                'title': 'Default',
                'begin': None,
                'end': None,
                'total': 0,
                'laps': 0
            }
        }

    def clocklapcount(self, _clockname='default'):
        """
        Get lap count for a given clock
        :param _clockname: clock name to retrieve lap count
        :type _clockname: str
        :return: lap count
        :rtype: int
        """
        return self._clocks[_clockname]['laps']

    def clocktotalsecs(self, _clockname='default'):
        """
        Get total time running for a given clock. Ignores if currently running
        :param _clockname: clock name to retrieve lap count
        :type _clockname: str
        :return: time running
        :rtype: int
        """
        return self._clocks[_clockname]['total']

    def addclock(self, _clockname, _clocktitle):
        """
        Add a new clock to the stopwatch
        :param _clocktitle: title for the clock
        :type _clocktitle: str
        :param _clockname: clockname
        :type _clockname: str
        """
        self._clocks[_clockname] = {
            'title': _clocktitle,
            'begin': None,
            'end': None,
            'total': 0,
            'laps': 0
        }

    def start(self, _clockname='default', overridestart=None):
        """
        Sets the start time
        As object can be reused, sets _end to None to ensure _end can't be before _begin
        :param overridestart: override the starttime if needbe
        :type overridestart: time.time()
        :param _clockname: clock name to start
        :type _clockname: str
        """
        _start = overridestart or time.time()
        if self.isstopped(_clockname):
            self._clocks[_clockname]['begin'] = _start
            self._clocks[_clockname]['end'] = None
        else:
            raise StopWatchException('StopWatch is already started')

    def startall(self):
        """
        Start all clocks at same time
        """
        _start = time.time()
        for _clock in self._clocks:
            self.start(_clock, overridestart=_start)

    def stop(self, _clockname='default', overrideend=None):
        """
        Sets the _end time and adds the difference between start and _end to the _total time so can have
        a running _total time (looping but only want to see how much part of the loop takes over all iterations)
        :param overrideend: overrid the end time if needbe
        :type overrideend: time.time()
        :param _clockname: clock name to start
        :type _clockname: str
        """
        _end = overrideend or time.time()
        if self.isstarted(_clockname):
            self._clocks[_clockname]['end'] = _end
            self._clocks[_clockname]['total'] += \
                int(self._clocks[_clockname]['end'] - self._clocks[_clockname]['begin'])
            self._clocks[_clockname]['laps'] += 1
        else:
            raise StopWatchException('StopWatch is already stopped.  It must be started first.')

    def stopall(self):
        """
        Stop all clocks at same time
        """
        _stop = time.time()
        for _clock in self._clocks:
            if self.isstarted(_clock):
                self.stop(_clock, overrideend=_stop)

    def reset(self, _clockname='default'):
        """Resets the StopWatch like it was never used
        :param _clockname: clock to reset
        :type _clockname: str
        """
        self._clocks[_clockname]['begin'] = self._clocks[_clockname]['end'] = None
        self._clocks[_clockname]['total'] = self._clocks[_clockname]['laps'] = 0

    def resetall(self):
        """
        Reset all clocks
        """
        for _clock in self._clocks:
            self.reset(_clock)

    def isstarted(self, _clockname='default'):
        """Determines if StopWatch is started
        Scenario 1: StopWatch was never used or not used since last reset (return False)
        Scenario 2: StopWatch was started and stopped (return False)
        Scenario 3: StopWatch was started but not stopped (return True)
        :param _clockname: clock to check
        :type _clockname: str
        :return: StopWatch start status
        :rtype: bool
        """
        if self._clocks[_clockname]['begin'] is not None and self._clocks[_clockname]['end'] is None:
            return True
        return False

    def startedclocks(self):
        """
        Get the clocks currently started/running
        :return: clocks running
        :rtype: list
        """
        return [_clock for _clock in self._clocks if self.isstarted(_clock)]

    def stoppedclocks(self):
        """
        Get the clocks currently stopped/not running
        :return: clocks stopped
        :rtype: list
        """
        return [_clock for _clock in self._clocks if self.isstopped(_clock)]

    def isstopped(self, _clockname='default'):
        """Determines if StopWatch is started and not stopped
        Scenario 1: StopWatch has been started at least once but not stopped (return False)
        Scenario 2: StopWatch has been started and stopped (return True)
        Scenario 3: StopWatch was never started or was reset (return True)
        :param _clockname: clock name
        :type _clockname: str
        :return: StopWatch stop status
        :rtype: bool
        """
        if self._clocks[_clockname]['end'] is not None and self._clocks[_clockname]['begin'] is not None \
                or not self.everused(_clockname):
            return True
        return False

    def everused(self, _clockname='default'):
        """Determines if the StopWatch has ever been started or started again since last reset
        :param _clockname: clock name
        :type _clockname: str
        :return: StopWatch used status
        :rtype: bool
        """
        if self._clocks[_clockname]['laps'] > 0 or self._clocks[_clockname]['begin'] is not None:
            return True
        return False

    def availableclocks(self):
        """
        Provides list of all clocks currently existing in stopwatch
        :return:
        """
        return self._clocks.keys()

    def usedclocks(self):
        """
        gets clocks that are currently in use
        """
        return [_clock for _clock in self._clocks if self.everused(_clock)]

    def reinitialize(self):
        """
        Returns stopwatch to original state where only a default clock exists
        :return:
        """
        # ensure default clock exists, if so reset it otherwise add it back
        if 'default' in self._clocks:
            self.reset()
        else:
            self.addclock('default', 'Default')
        # remove all other clocks
        for clock in [x for x in self._clocks if x != 'default']:
            self.removeclock(clock)

    def removeclock(self, _clockname):
        """
        Removes the clock designated by clock name.  Throws error if trying to delete last clock
        :param _clockname:
        :return:
        """
        if len(self._clocks) > 1:
            del self._clocks[_clockname]
        else:
            raise StopWatchException('Not allowed to remove last clock')

    @staticmethod
    def __humanreadabletime(_secs):
        _days = _hrs = _mins = 0.0
        _timestr = ''
        if _secs >= 60.0:
            _mins = _secs // 60.0
            _secs %= 60.0
        if _mins >= 60.0:
            _hrs = _mins // 60.0
            _mins %= 60.0
        if _hrs >= 24.0:
            _days = _hrs // 24.0
            _hrs %= 24.0
        if _days > 0:
            _timestr += '%s days ' % _days
        if _hrs > 0:
            _timestr += '%s hours ' % _hrs
        if _mins > 0:
            _timestr += '%s minutes ' % _mins
        if _secs > 0:
            _timestr += '%s seconds' % _secs
        return _timestr

    def get_clock_summary(self, onlytime=False, _clockname='default'):
        """
        Retrieves the duration seen from start to _end.  Prepends a custom label if provided
        :param onlytime: only return time portion
        :type onlytime: bool
        :param _clockname: name of clock
        :type _clockname: str
        :return: nicely formatted duration string
        :rtype: str
        """
        if not self.everused(_clockname):
            _msg = 'StopWatch never used.'
        elif self._clocks[_clockname]['end'] is None:
            raise StopWatchException('StopWatch must be stopped before a duration can be calculated')
        else:
            _timestr = self.__humanreadabletime(self._clocks[_clockname]['total'])
            if onlytime:
                _msg = _timestr
            else:
                _msg = '%s: Duration: %s in %s lap(s).' % \
                       (self._clocks[_clockname]['title'], _timestr, self._clocks[_clockname]['laps'])
        return _msg

    @property
    def summary(self):
        """
        Get summary for stopwatch as a whole
        :return: str
        """
        _msg = ''
        _total = 0
        _msg += 'Summary for %s stop watch' % self.title
        _msg += '%s\n' % '=' * 90
        for _clock in self._clocks:
            _msg += '%s\n' % self.get_clock_summary(_clockname=_clock)
            _total += self._clocks[_clock]['total']
        _msg += '%s\n' % '=' * 90
        _msg += 'Total Duration: %s' % self.__humanreadabletime(_total)
        return _msg

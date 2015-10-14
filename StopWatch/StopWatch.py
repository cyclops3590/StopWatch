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

    def __init__(self):
        """
        initialize StopWatch object instance
        :var self._begin: time of last start
        :type self._begin: timestamp
        :var self._end: time of last stop
        :type self._end: timestamp
        :var self._total: total time in seconds the stopwatch has ran (as of last stop)
        :type self._total: int
        :var self._cycles: number of times stopwatch has been started and stopped since init or last reset
        :type self._cycles: int
        :return: n/a
        """
        self._begin = None
        self._end = None
        self._total = 0
        self._cycles = 0

    def start(self):
        """
        Sets the start time
        As object can be reused, sets _end to None to ensure _end can't be before _begin
        """
        if self.isstopped():
            self._begin = time.time()
            self._end = None
        else:
            raise StopWatchException('StopWatch is already started')

    def stop(self):
        """
        Sets the _end time and adds the difference between start and _end to the _total time so can have
        a running _total time (looping but only want to see how much part of the loop takes over all iterations)
        """
        if self.isstarted():
            self._end = time.time()
            self._total += int(self._end - self._begin)
            self._cycles += 1
        else:
            raise StopWatchException('StopWatch is already stopped.  It must be started first.')

    def reset(self):
        """Resets the StopWatch like it was never used"""
        self._begin = self._end = None
        self._total = self._cycles = 0

    def isstarted(self):
        """Determines if StopWatch is started
        Scenario 1: StopWatch was never used or not used since last reset (return False)
        Scenario 2: StopWatch was started and stopped (return False)
        Scenario 3: StopWatch was started but not stopped (return True)
        :return: StopWatch start status
        :rtype: bool
        """
        if self._begin is not None and self._end is None:
            return True
        return False

    def isstopped(self):
        """Determines if StopWatch is started and not stopped
        Scenario 1: StopWatch has been started at least once but not stopped (return False)
        Scenario 2: StopWatch has been started and stopped (return True)
        Scenario 3: StopWatch was never started or was reset (return True)
        :return: StopWatch stop status
        :rtype: bool
        """
        if self._end is not None and self._begin is not None \
                or not self.everused():
            return True
        return False

    def everused(self):
        """Determines if the StopWatch has ever been started or started again since last reset
        :return: StopWatch used status
        :rtype: bool
        """
        if self._cycles > 0 or self._begin is not None:
            return True
        return False

    @staticmethod
    def __timecalc(_secs):
        """
        Converts seconds into a list for days, hours, minutes, seconds
        :param _secs: number of seconds to 'humanize'
        :type _secs: int
        :return: list specifying days, hours, minutes, seconds
        :rtype: list
        """
        _days = _hrs = _mins = 0.0
        if _secs >= 60.0:
            _mins = _secs // 60.0
            _secs %= 60.0
        if _mins >= 60.0:
            _hrs = _mins // 60.0
            _mins %= 60.0
        if _hrs >= 24.0:
            _days = _hrs // 24.0
            _hrs %= 24.0
        return [_days, _hrs, _mins, _secs]

    def print_duration(self, _label='', onlytime=False):
        """
        Prints the duration seen from start to _end.  Pre-p_ends a custom label if provided
        :param onlytime: print time only (true) or laps, label as well (false)
        :type onlytime: bool
        :param _label: used to customize the duration string when printed
        :type _label: basestring
        :return: nicely formatted duration string
        :rtype: basestring
        """
        if not self.everused():
            _msg = 'StopWatch never used.'
        elif self._end is None:
            raise StopWatchException('StopWatch must be stopped before a duration can be calculated')
        else:
            _d, _h, _m, _s = self.__timecalc(round(int(self._total), 3))
            _timestr = ''
            if _d > 0:
                _timestr += '%s days ' % _d
            if _h > 0:
                _timestr += '%s hours ' % _h
            if _m > 0:
                _timestr += '%s minutes ' % _m
            if _s > 0:
                _timestr += '%s seconds' % _s
            if _label != '':
                _label += ' '
            if _timestr == '':
                _timestr = '%s seconds' % self._total
            if onlytime:
                _msg = _timestr
            else:
                _msg = 'STOPWATCH: %sDuration: %s in %s lap(s).' % (_label, _timestr, self._cycles)
        return _msg
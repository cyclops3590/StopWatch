# coding=utf-8
"""
This class simplifies the interactions needed to determine the time code chunks take to operate.
"""

from datetime import datetime
from .StopWatchException import StopWatchException, StopWatchLapException

class Lap(object):

    def __init__(self):
        self.paused = False
        self.total = 0.0
        self.starttime = None
        self.endtime = None

    def pause(self,_override=None):
        if self.ispaused():
            raise StopWatchLapException('Cannot pause a lap that is paused')
        end = _override or datetime.utcnow()
        self.paused = True
        _d = end - self.starttime
        self.total += _d.total_seconds()
        self.starttime = None
        self.endtime = None

    def unpause(self,_override=None):
        if not self.ispaused():
            raise StopWatchLapException('Cannot unpause a lap that is not paused')
        self.starttime = _override or datetime.utcnow()
        self.paused = False

    def start(self,_override=None):
        if self.isstarted():
            raise StopWatchLapException('Cannot start a lap already started')
        elif self.ispaused():
            self.paused = False
        self.starttime = _override or datetime.utcnow()

    def stop(self, _override=None):
        if self.isstopped():
            # not paused, not started
            raise StopWatchLapException('Cannot stop lap that is not started')
        elif self.ispaused():
            self.paused = False
        else:
            self.endtime = _override or datetime.utcnow()
            _d = self.endtime - self.starttime
            self.total += _d.total_seconds()
            self.starttime = None
            self.endtime = None
            self.paused = False

    def laptotalsecs(self):
        return self.total

    def isstarted(self):
        if self.starttime is not None or self.paused is True:
            return True
        return False

    def ispaused(self):
        return self.paused

    def isstopped(self):
        if not self.isstarted() and not self.ispaused():
            return True
        return False





class StopWatch(object):
    """
    Class definition for StopWatch which is a class to simply perform start, stop and print duration strings.
    This takes care of slightly redundant and more complex logic to provide an easy interface for
    stopwatch functionality
    """

    def __init__(self, _swtitle='StopWatch Default', _defaulttitle='default', _defaultname='default', _recordlapdetail=False):
        """
        initialize StopWatch object instance
        :param _swtitle: Title for the stop watch
        :type _swtitle: str
        :var self._clocks: various clocks being tracked.  'default' is only one setup immediately
        :type self._clocks: dict
        :return: n/a
        """
        self.title = _swtitle
        self._defaulttitle = _defaulttitle
        self._defaultname = _defaultname
        self._clocks = self.__init_clock(self._defaultname, self._defaulttitle)
        self._recordlapdetail = _recordlapdetail

    def __init_clock(self, _name, _title, _display=True):
        return {
            _name: {
                'title': _title,
                'begin': None,
                'end': None,
                'total': 0.0,
                'laps': 0,
                'lapdetail': [],
                'currentlap': 0,
                'display': _display,
                'paused': False
            }
        }

    def clocklapcount(self, _clockname=None):
        """
        Get lap count for a given clock; includes current lap if running
        :param _clockname: clock name to retrieve lap count
        :type _clockname: str
        :return: lap count
        :rtype: int
        """
        _clockname = _clockname or self._defaultname
        return self._clocks[_clockname]['currentlap']

    def clocktotalsecs(self, _clockname=''):
        """
        Get total time running for a given clock.  Including current lap if running
        :param _clockname: clock name to retrieve lap count
        :type _clockname: str
        :return: time running
        :rtype: int
        """
        if not _clockname:
            _clockname = self._defaultname
        _time = self._clocks[_clockname]['total']
        if self.isstarted(_clockname):
            _time += (datetime.utcnow() - self._clocks[_clockname]['begin']).total_seconds()
        return float(_time)

    def addclock(self, _clockname, _clocktitle, _display=True):
        """
        Add a new clock to the stopwatch
        :param _display:
        :param _clocktitle: title for the clock
        :type _clocktitle: str
        :param _clockname: clockname
        :type _clockname: str
        """
        self._clocks.update(self.__init_clock(_clockname, _clocktitle, _display))

    def start(self, _clockname=None, overridestart=None):
        """
        Sets the start time
        As object can be reused, sets _end to None to ensure _end can't be before _begin
        :param overridestart: override the starttime if needbe
        :type overridestart: datetime.utcnow()
        :param _clockname: clock name to start
        :type _clockname: str
        """
        if not _clockname:
            _clockname = self._defaultname
        _start = overridestart or datetime.utcnow()
        if self.isstopped(_clockname):
            self._clocks[_clockname]['begin'] = _start
            self._clocks[_clockname]['end'] = None
            self._clocks[_clockname]['currentlap'] += 1
            if self._recordlapdetail:
                self._clocks[_clockname]['lapdetail'].append(Lap())
                self._clocks[_clockname]['lapdetail'][-1].start(_start)
        elif self.ispaused(_clockname):
            raise StopWatchException('StopWatch is currently paused')
        else:
            raise StopWatchException('StopWatch is already started')

    def startall(self):
        """
        Start all clocks at same time
        """
        _start = datetime.utcnow()
        for _clock in self._clocks:
            self.start(_clock, overridestart=_start)

    def stop(self, _clockname=None, overrideend=None):
        """
        Sets the _end time and adds the difference between start and _end to the _total time so can have
        a running _total time (looping but only want to see how much part of the loop takes over all iterations)
        :param overrideend: overrid the end time if needbe
        :type overrideend: datetime.utcnow()
        :param _clockname: clock name to start
        :type _clockname: str
        """
        if not _clockname:
            _clockname = self._defaultname
        _end = overrideend or datetime.utcnow()
        if self.ispaused(_clockname):
            self._clocks[_clockname]['laps'] += 1
            self._clocks[_clockname]['paused'] = False
            if self._recordlapdetail:
                self._clocks[_clockname]['lapdetail'][-1].stop(_end)
        elif self.isstarted(_clockname):
            self._clocks[_clockname]['end'] = _end
            self._clocks[_clockname]['total'] += (self._clocks[_clockname].get('end') - self._clocks[_clockname].get('begin')).total_seconds()
            self._clocks[_clockname]['laps'] += 1
            if self._recordlapdetail:
                self._clocks[_clockname]['lapdetail'][-1].stop(_end)
        else:
            raise StopWatchException('StopWatch is already stopped.  It must be started first.')

    def pause(self, _clockname=None, overrideend=None):
        """
        Pauses the clock.  This makes it so laps will be more reflective of desired behavior and the time is as desired
        as well
        :param overrideend:
        :param _clockname:
        :return:
        """
        _clockname = _clockname or self._defaultname
        _end = overrideend or datetime.utcnow()
        if self.ispaused(_clockname):
            raise StopWatchException('StopWatch clock, {0}, is already paused.  It must be unpaused first.'
                                     .format(_clockname))
        elif self.isstarted(_clockname):
            self._clocks[_clockname]['end'] = _end
            self._clocks[_clockname]['total'] += \
                (_end - self._clocks[_clockname]['begin']).total_seconds()

            self._clocks[_clockname]['paused'] = True
            if self._recordlapdetail:
                self._clocks[_clockname]['lapdetail'][-1].pause(_end)
        else:
            raise StopWatchException('StopWatch clock, {0}, is already stopped.  It must be started first.'
                                     .format(_clockname))

    def unpause(self, _clockname=None, overridestart=None):
        """
        Unpause a paused clock
        :param _clockname:
        :param overridestart:
        :return:
        """
        if not _clockname:
            _clockname = self._defaultname
        _start = overridestart or datetime.utcnow()
        if self.ispaused(_clockname):
            self._clocks[_clockname].update({
                'begin': _start,
                'end': None,
                'paused': False
            })
            if self._recordlapdetail:
                self._clocks[_clockname]['lapdetail'][-1].unpause(_start)
        else:
            raise StopWatchException('StopWatch is not paused')

    def ispaused(self, _clockname=None):
        """
        Check if a clock is paused
        :param _clockname:
        :return:
        """
        clockname = _clockname or self._defaultname
        return self._clocks[clockname]['paused']


    def stopall(self):
        """
        Stop all clocks at same time
        """
        _stop = datetime.utcnow()
        for _clock in self._clocks:
            if self.isstarted(_clock):
                self.stop(_clock, overrideend=_stop)

    def reset(self, _clockname=None):
        """Resets the StopWatch like it was never used
        :param _clockname: clock to reset
        :type _clockname: str
        """
        if not _clockname:
            _clockname = self._defaultname
        self._clocks.update(self.__init_clock(_clockname, self._clocks[_clockname]['title']))

    def resetall(self):
        """
        Reset all clocks
        """
        for _clock in self._clocks:
            self.reset(_clock)

    def isstarted(self, _clockname=None):
        """Determines if StopWatch is started
        Scenario 1: StopWatch was never used or not used since last reset (return False)
        Scenario 2: StopWatch was started and stopped (return False)
        Scenario 3: StopWatch was started but not stopped (return True)
        :param _clockname: clock to check
        :type _clockname: str
        :return: StopWatch start status
        :rtype: bool
        """
        if not _clockname:
            _clockname = self._defaultname
        if self._clocks[_clockname]['begin'] is not None and self._clocks[_clockname]['end'] is None or self._clocks[_clockname]['paused']:
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

    def pausedclocks(self):
        """
        Get the clocks currently paused
        :return: clocks stopped
        :rtype: list
        """
        return [_clock for _clock in self._clocks if self.ispaused(_clock)]

    def isstopped(self, _clockname=None):
        """Determines if StopWatch is started and not stopped
        Scenario 1: StopWatch has been started at least once but not stopped (return False)
        Scenario 2: StopWatch has been started and stopped (return True)
        Scenario 3: StopWatch was never started or was reset (return True)
        :param _clockname: clock name
        :type _clockname: str
        :return: StopWatch stop status
        :rtype: bool
        """
        _clockname = _clockname or self._defaultname
        if self._clocks[_clockname]['end'] is not None and self._clocks[_clockname]['begin'] is not None and self._clocks[_clockname]['paused'] is False \
                or not self.everused(_clockname):
            return True
        return False

    def everused(self, _clockname=None):
        """Determines if the StopWatch has ever been started or started again since last reset
        :param _clockname: clock name
        :type _clockname: str
        :return: StopWatch used status
        :rtype: bool
        """
        _clockname = _clockname or self._defaultname
        if self.clocklapcount(_clockname) > 0 or self._clocks[_clockname]['begin'] is not None:
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

    def haslapdetail(self):
        return self._recordlapdetail

    def lapdetail(self,lapnumber,_clockname=None):
        if not _clockname:
            _clockname = self._defaultname

        if self._recordlapdetail is False:
            raise StopWatchException('Lap detail not recorded')
        elif lapnumber <= 0 or lapnumber > len(self._clocks[_clockname]['lapdetail']):
            raise StopWatchException('Lap {0} is invalid'.format(lapnumber))
        else:
            _lapobj = self._clocks[_clockname]['lapdetail'][lapnumber-1]
            return {
                'total': _lapobj.laptotalsecs(),
                'ispaused': _lapobj.ispaused(),
                'isstarted': _lapobj.isstarted()
            }

    def reinitialize(self):
        """
        Returns stopwatch to original state where only a default clock exists
        :return:
        """
        # ensure default clock exists, if so reset it otherwise add it back
        if self._defaultname in self._clocks:
            self.reset()
        else:
            self.addclock(self._defaultname, self._defaulttitle)
        # remove all other clocks
        for clock in [x for x in self._clocks if x != self._defaultname]:
            self.removeclock(clock)

    def removeclock(self, _clockname):
        """
        Removes the clock designated by clock name.  Throws error if trying to delete last clock
        :param _clockname:
        :return:
        """
        if _clockname in self._clocks:
            del self._clocks[_clockname]
        else:
            raise StopWatchException('Clock, {0}, does not exist'.format(_clockname))

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
            _timestr = '{0}{1} days '.format(_timestr, int(_days))
        if _hrs > 0:
            _timestr = '{0}{1} hours '.format(_timestr, int(_hrs))
        if _mins > 0:
            _timestr = '{0}{1} minutes '.format(_timestr, int(_mins))
        if _secs > 0:
            _timestr = '{0}{1} seconds'.format(_timestr, '{0:f}'.format(_secs))
        if not _timestr:
            _timestr = '{0:f} seconds'.format(_secs)
        return _timestr

    def get_clock_detail(self,_clockname=None):
        if not _clockname:
            _clockname = self._defaultname
        if not self.everused(_clockname):
            _msg = '{0}: StopWatch never used.'.format(self._clocks[_clockname]['title'])
        elif self._clocks[_clockname]['end'] is None:
            raise StopWatchException('StopWatch must be stopped before a duration can be calculated')
        else:
            _timestr = self.__humanreadabletime(self._clocks[_clockname]['total'])
            _msg = '{0}: Duration: {1}\n'.format(self._clocks[_clockname]['title'], _timestr)
            _lapfmt = '    Lap {0}: {1}\n'
            for _lapidx in range(len(self._clocks[_clockname]['lapdetail'])):
                _lapobj = self._clocks[_clockname]['lapdetail'][_lapidx]
                _msg += _lapfmt.format(_lapidx,_lapobj.laptotalsecs())
        return _msg

    def get_clock_summary(self, onlytime=False, _clockname=None, printlaps=True, json=False):
        """
        Retrieves the duration seen from start to _end.  Prepends a custom label if provided
        :param json:
        :param printlaps:
        :param onlytime: only return time portion
        :type onlytime: bool
        :param _clockname: name of clock
        :type _clockname: str
        :return: nicely formatted duration string
        :rtype: str
        """
        if not _clockname:
            _clockname = self._defaultname
        if not self.everused(_clockname):
            _msg = '{0}: StopWatch never used.'.format(self._clocks[_clockname]['title'])
        elif self._clocks[_clockname]['end'] is None:
            raise StopWatchException('StopWatch must be stopped before a duration can be calculated')
        else:
            _timestr = self.__humanreadabletime(self._clocks[_clockname]['total'])
            if onlytime:
                _msg = _timestr
            else:
                _msg = '{0}: Duration: {1}'.format(self._clocks[_clockname]['title'], _timestr)
                if printlaps:
                    _msg = '{0} in {1} lap(s)'.format(_msg, self._clocks[_clockname]['currentlap'])
        return _msg

    @property
    def summary(self):
        return self.get_summary()

    def get_summary(self, json=False, _displayall=False,default_is_overall=False):
        """
        Get summary for stopwatch as a whole
        :return: str
        """
        if json:
            _msg = {
                'Overall': {
                  'total': 0,
                },
                'Combined': {
                    'total': 0,
                },
                'Hidden': {
                    'title': 'Hidden',
                    'count': 0,
                    'total': 0.0,
                    'laps': 0
                },
            }
            for _clockname in self._clocks:
                _clock = self._clocks[_clockname]
                _msg['Combined']['total'] += self.clocktotalsecs(_clockname)
                if _displayall or _clock['display']:
                    if default_is_overall and _clockname == self._defaultname:
                        _msg['Overall']['total'] = self.clocktotalsecs(_clockname)
                    elif not default_is_overall:
                        _msg['Overall']['total'] += self.clocktotalsecs(_clockname)
                    _msg[_clockname] = {
                        'title': _clock['title'],
                        'total': self.clocktotalsecs(_clockname),
                        'laps': self.clocklapcount(_clockname)
                    }
                else:
                    _msg['Hidden']['count'] += 1
                    _msg['Hidden']['total'] += self.clocktotalsecs(_clockname)
                    _msg['Hidden']['laps'] += self.clocklapcount(_clockname)
        else:
            _msg = 'Summary for {0} stop watch\n'.format(self.title)
            _msg = '{0}{1}\n'.format(_msg, '=' * 90)
            hiddencount = 0
            hiddentime = 0.0
            hiddenlaps = 0
            _combined = 0
            _overall = 0
            for _clockname in self._clocks:
                if _displayall or self._clocks[_clockname]['display']:
                    _msg = '{0}{1}\n'.format(_msg, self.get_clock_summary(_clockname=_clockname))
                else:
                    hiddencount += 1
                    hiddentime += self.clocktotalsecs(_clockname)
                    hiddenlaps += self.clocklapcount(_clockname)
                if default_is_overall and _clockname == self._defaultname:
                    _overall = self.clocktotalsecs(_clockname)
                elif not default_is_overall:
                    _overall += self.clocktotalsecs(_clockname)
                _combined += self.clocktotalsecs(_clockname)
            if hiddencount > 0:
                _msg = '{0}{4}\n{1} Hidden Clock(s): {2:f} seconds in {3} lap(s)\n'.format(_msg, hiddencount,
                                                                                           hiddentime, hiddenlaps,
                                                                                           '-' * 90)
            _msg = '{0}{1}\n'.format(_msg, '=' * 90)
            _msg = '{0}Total Duration: {1}'.format(_msg, self.__humanreadabletime(_overall))
            if default_is_overall:
                _msg = '{0}Total Duration (All Clocks): {1}'.format(_msg, self.__humanreadabletime(_combined))
        return _msg


def timeit(logger=None, level='debug'):
    """
    decorator to time a function in general.  Takes optional logging module instance and logging level
    None means print to stdout
    :param level:
    :param logger:
    :return:
    """

    def decorator(func):
        """

        :param func:
        :return:
        """

        def wrapper(*args, **kwargs):
            """

            :param args:
            :param kwargs:
            :return:
            """
            _sw = StopWatch(_defaultname='decorator', _defaulttitle=func.__name__)
            _sw.start()
            _output = func(*args, **kwargs)
            _sw.stop()
            if logger:
                getattr(logger, level.lower())(_sw.get_clock_summary(_clockname='decorator', printlaps=False))
            else:
                print(_sw.get_clock_summary(_clockname='decorator', printlaps=False))
            return _output

        return wrapper

    return decorator

========================
StopWatch - Multi-clock
========================


StopWatch is meant to provide an easy interface to stopwatch like functionality within code.  However, instead of a single clock, it can do multiple clocks, each with their own label/title and properties.

This was meant to help keep track of how long parts of code execute.  Because there are times where you want to see only a portion of the code runs within a loop and don't want the complexity of instantiating, tracking, etc. variables yourself, this helps abstract that complexity away and still give what you want.


Feature Summary
-----------------

1. Multiple clocks within one stopwatch
2. Multiple laps allowed per clock
3. Create summary message per clock or for entire stopwatch
4. Retrieve summary time for clock in human readable or epoch formats
5. Decorator to time individual functions (and log to specified destination)

Installing
------------

From the command line::

    pip install StopWatch

If StopWatch is already installed, you can upgrade to the latest version with::

    pip install --upgrade StopWatch

Usage
-------

StopWatch (all commands demo'ed)::

    sw = StopWatch('StopWatch Title','Default Clock Name','Default Clock Title')
    sw.addclock('newclock1','New Clock 1')
    sw.start('newclock1')
    sw.start()
    sw.addclock('newclock2','New Clock 2')
    sw.stop('newclock1')
    sw.startall()
    sw.stopall()
    if sw.isstarted('newclock2'):
        print('newclock2 is started')
    elif sw.isstopped('newclock2'):
        print('newclock2 is stopped')
    if sw.everused():
        print('default clock was used at least once.')
    print('newclock1 ran %s laps for %s seconds' % (sw.clocklapcount('newclock1'),sw.clocktotalsecs('newclock1'))
    sw.reset('newclock2')
    sw.resetall()
    print('started clocks: %s' % sw.startedclocks())
    print('stopped clocks: %s' % sw.stoppedclocks())
    print('used clocks: %s' % sw.usedclocks())
    print('all clocks in stopwatch: %s' % sw.availableclocks())
    sw.removeclock('newclock1')
    print(sw.get_clock_summary(_clockname='newclock2'))
    print(sw.summary())
    sw.reinitialize()
    
timeit decorator::

Will log the clock summary to logger at info level

    @timeit(logger,'info')
    def ping100(ip):
        os.system('ping -c 100 %s' % ip)

Feedback
--------

Feel free to send any feedback you may have regarding this project to cyclops3590@gmail.com.
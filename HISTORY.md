# Changelog

## 0.9.0 (2018-04-02)

### New

* Allow for default clock to be considered the overall time for summary (#8) [cyclops3590]

### Changes

* Get everything up to date (#7) [cyclops3590]

  * No timestring was returnged if 0 seconds.
  * Summary strings had new line in bad place
  * Convert strings with variables to new format style
  * Summary wasn't printing as expected.
  * Added overall timing to summary.
  * Added json format for output
  * Add ability to pause a clock
  * Changed to datetime to provide far greater precision
  * Pausing wasn't updated for using datetime
  * Retrieving clock seconds was still in scientific format for some numbers
  * Add Python 3.x compatibility
  * Switched to unittest
  * Add detail on a per lap basis
  * Add travis CI integration for testing


## 0.4.5 (2017-01-24)

### New

* Python 3.x compatibility change. [Marc Grosz]

### Fix

* Pausing wasn't updated for using datetime.  retrieving clock seconds was still in scientific format for some numbers. [cyclops]


## 0.4.4 (2017-01-13)

### New

* Add manual verification tests.  summary print out needs to be validated for format. [cyclops]

* Changed to datetime to provide far greater precision. [cyclops]


## 0.4.3 (2016-09-30)

### New

* Add ability to pause a clock. [cyclops3590]

### Changes

* Convert strings with variables to new format style. [cyclops]

### Fix

* Summary wasn't printing as expected.  Added overall timing to summary.  Added json format for output. [cyclops]

* No timestring was returned if 0 seconds. Summary strings had new line in bad place. [cyclops]


## 0.4.0 (2016-01-21)

### New

* Finalize pypi ability. [cyclops]

* Make default clock more dynamic.  add decorator to time a function. [cyclops]

### Changes

* Code compliance fixes. [cyclops]

* Readying for pypi. [cyclops]


## 0.3.0 (2016-01-20)

### New

* Added tests for multiclock stopwatch. [cyclops]

* Add ability to remove a clock and to reinit the entire stopwatch. [cyclops]

### Fix

* Stopping all clocks now works as intended.  optimized other code. added function to retrieve available clocks in stopwatch. [cyclops]

* Changelog. [cyclops]


## 0.2.2 (2015-10-14)

### Fix

* Correct 2 test cases. [cyclops]


## 0.2.0 (2015-10-14)

### New

* Added initial testing. [cyclops]

* Added ability to have multiple clocks within a single stopwatch. [cyclops]

### Fix

* Various small bugs/format issues. [cyclops]


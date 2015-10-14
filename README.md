
# README

### Purpose

StopWatch is meant to provide an easy interface to stopwatch like functionality within code.  However, instead of a single clock, it can do multiple clocks, each with their own label/title and properties.

This was meant to help keep track of how long parts of code execute.  Because there are times where you want to see only a portion of the code runs within a loop and don't want the complexity of instantiating, tracking, etc. variables yourself, this helps abstract that complexity away and still give what you want.

### Features

Each clock has standard stop watch capabilities for the most part.  It keeps track of lap count and total time the clock has ran.  Currently it does not keep track of time per lap like can be helpful when using a stop watch for racing.  Due to the original purpose of this package it was deemed unnecessary that per lap times would be useful.  However it can be easily added so message me if you think its worth that little effort.  Each clock has its own label as well since each clock is designed to track a specific part of code; e.g. DB call, processing results, etc.

You can have multiple clocks as well.  Since each clock has its own title, you can track each clock separately; however, have a single stop watch to track everything which can then provide a summary that states how long each clock (part of code) ran as well as how long all clocks ran.  Keep in mind the stopwatch total is equal to the sum of the individual clocks so depending on how you use them your stop watch total could be higher than your actual total runtime so make sure to use them as designed.



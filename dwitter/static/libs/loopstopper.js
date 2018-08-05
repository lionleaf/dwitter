window.stopper = {

  loops: [],
  loopTimers: [],
  TIME_OUT_LENGTH: 4000,
  states: Object.freeze({ 
    UNMONITORED: 0,
    MONITORED: 1,
    FINISHED: 2,
    INFINITE: 3 
  }),
  // States:
  //   undefined/0 - unmonitored
  //   1           - Currently being monitored
  //   2           - Finished
  //   3           - Infinite
  // restartLoop moves the loop from state 0 and 2 to 1
  // testLoop returns true, if the loop was found to be infinite or it takes too much time
  // exitLoop moves the loop to a finished state (state 2)

  reset: function() {
    this.loops = [];
    this.loopTimers = [];
  },
  restartLoop: function(loopId) {
    if (typeof this.loops[loopId] === "undefined" || this.loops[loopId] == this.states.UNMONITORED || this.loops[loopId] == this.states.FINISHED) {
      this.loops[loopId] = this.states.MONITORED;
      this.loopTimers[loopId] = Date.now();
    }
  },
  testLoop: function(loopId) {
    if (this.loops[loopId] == this.states.INFINITE)
      return true;
    if (this.loops[loopId] == this.states.MONITORED) {
      if (Date.now() - this.loopTimers[loopId] > this.TIME_OUT_LENGTH) {
        this.loops[loopId] = this.states.INFINITE;
        return true;
      } else {
        return false;
      }
    }
    return false;
  },
  exitLoop: function(loopId) {
    if (this.loops[loopId] == this.states.MONITORED) {
      this.loops[loopId] = this.states.FINISHED;
    }
  }

}

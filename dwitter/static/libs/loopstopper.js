window.stopper = {

  loops: [],
  loopTimers: [],
  TIME_OUT_LENGTH: 500,

  // States:
  // undefined/0 - unmonitored
  // 1           - Currently being monitored
  // 2           - Exited
  // 3           - Infinite

  reset: function() {
    this.loops = [];
    this.loopTimers = [];
  },
  restartLoop: function(loopId) {
    if (!this.loops[loopId] || this.loops[loopId] == 2) {
      this.loops[loopId] = 1;
      this.loopTimers[loopId] = Date.now();
    }
  },
  testLoop: function(loopId) {
    if (this.loops[loopId] == 3)
      return true;
    if (this.loops[loopId] == 1) {
      if (Date.now() - this.loopTimers[loopId] > this.TIME_OUT_LENGTH) {
        this.loops[loopId] = 3;
        return true;
        console.log(1);
      } else {
        return false;
      }
    }
    return false;
  },
  exitLoop: function(loopId) {
    if (this.loops[loopId] == 1) {
      this.loops[loopId] = 2;
    }
  }

}

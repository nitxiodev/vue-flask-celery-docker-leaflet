import store from "./store";
export default {
  computed: {
    running: function() {
      return false;
    }
  },
  beforeRouteLeave(to, from, next) {
    // called when the route that renders this component is about to
    // be navigated away from.
    // has access to `this` component instance.
    let answer = !this.running;

    if (this.running) {
      answer = window.confirm(
        "Do you really want to leave? If you do that, you will lose all current data!"
      );
    }

    if (answer) {
      store.commit("CLEAR_RUNS");
      next();
    } else {
      next(false);
    }
  }
};

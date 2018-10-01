export const UPDATE_ME = (state, me) => {
  state.me = me;
};

export const UPDATE_LOCATION = (state, location) => {
  state.location = location;
};

export const UPDATE_SUDOKU = (state, runSudoku) => {
  state.runSudoku = runSudoku;
};

export const UPDATE_MAP = (state, runMap) => {
  state.runMap = runMap;
};

export const CLEAR_RUNS = state => {
  state.runMap = false;
  state.runSudoku = false;
};

/**
 * Clear each property, one by one, so reactivity still works.
 *
 * (ie. clear out state.auth.isLoggedIn so Navbar component automatically reacts to logged out state,
 * and the Navbar menu adjusts accordingly)
 *
 * TODO: use a common import of default state to reset these values with.
 */
export const CLEAR_ALL_DATA = state => {
  state.me = null;
};

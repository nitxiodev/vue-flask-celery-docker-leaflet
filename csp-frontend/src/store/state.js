// export const STORAGE_KEY = 'csp_cloud';

let memoryData = {
  me: null,
  location: null,
  runSudoku: false,
  runMap: false
};

let sessionData = {
  lang: null
};

// Sync with session storage.
// if (sessionStorage.getItem(STORAGE_KEY)) {
//   sessionData = JSON.parse(sessionStorage.getItem(STORAGE_KEY))
// }

// Merge data and export it.
export const state = Object.assign(memoryData, sessionData);

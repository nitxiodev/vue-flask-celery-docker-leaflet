const sessionStoragePlugin = store => {
  store.subscribe((mutation, state) => {
    console.log("MUTATION ", mutation, state);
  });
};
const memoryStoragePlugin = store => {
  store.subscribe((mutation, state) => {
    console.log("MUTATION ", mutation, state);
  });
};

export default [memoryStoragePlugin, sessionStoragePlugin];

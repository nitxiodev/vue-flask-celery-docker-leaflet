import L from "leaflet";

export default {
  install(Vue) {
    Vue.prototype.$L = Vue.L = L;
  }
};

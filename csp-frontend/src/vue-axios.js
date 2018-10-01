import axios from "axios";

export default {
  install(Vue) {
    Vue.prototype.$http = Vue.http = axios;
  }
};

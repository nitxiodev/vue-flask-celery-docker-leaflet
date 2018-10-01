import Vue from "vue";
import App from "./App.vue";
import router from "./router";
// import store from "./___store";
import axios from "./vue-axios"; // Axios plugin
import leaflet from "./vue-leaflet";
import VeeValidate from "vee-validate";
require("../node_modules/bootstrap/dist/js/bootstrap.bundle.min");
require("./prototypes");
import VueSocketio from "vue-socket.io";
import store from "./store";

Vue.config.productionTip = false;
Vue.use(axios);
Vue.use(leaflet);
Vue.use(VeeValidate);

// https://github.com/KoRiGaN/Vue2Leaflet/issues/157
delete Vue.L.Icon.Default.prototype._getIconUrl;

Vue.L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("../node_modules/leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("../node_modules/leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("../node_modules/leaflet/dist/images/marker-shadow.png")
});

async function configuration() {
  let config = await Vue.http.get("./static/config.json");
  console.log("CONFIG", config.data);
  Vue.http.defaults.baseURL = config.data.rest_url;
  Vue.use(VueSocketio, config.data.socketio_url);

  new Vue({
    router,
    store,
    render: h => h(App)
  }).$mount("#app");
}

configuration();

// Vue.http.defaults.baseURL = "http://localhost:8888";
//
// new Vue({
//   router,
//   store,
//   render: h => h(App)
// }).$mount("#app");

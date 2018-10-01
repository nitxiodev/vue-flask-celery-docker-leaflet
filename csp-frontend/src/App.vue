<template>
  <div id="app">
    <v-main></v-main>
  </div>
</template>

<script>
import Main from "@/components/Main.vue";
export default {
  name: "app",
  components: {
    "v-main": Main
  }
};
</script>

<style>
@import "../node_modules/leaflet/dist/leaflet.css";
@import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
* {
  margin: 0;
  padding: 0;
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*text-align: center;*/
  color: #2c3e50;
}

/*#nav {*/
/*padding: 30px;*/
/*}*/

/*#nav a {*/
/*font-weight: bold;*/
/*color: #2c3e50;*/
/*}*/

/*#nav a.router-link-exact-active {*/
/*color: #42b983;*/
/*}*/
.btn-circle {
  width: 40px;
  height: 40px;
  text-align: center;
  padding: 6px 0;
  font-size: 15px;
  line-height: 1.42857;
  border-radius: 20px;
}
.btn-default:hover:not(:disabled) {
  background-color: #babfb8;
  border-color: #a3a9a0;
}
</style>

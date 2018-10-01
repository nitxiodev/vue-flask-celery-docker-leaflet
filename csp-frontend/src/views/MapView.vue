<template>
  <div class="row">
    <Map></Map>
  </div>
</template>

<script>
// @ is an alias to /src
import Map from "@/components/Map.vue";
import store from "../store";
import mixin from "../viewMixin";

export default {
  name: "home",
  mixins: [mixin],
  components: {
    Map
  },
  computed: {
    running: function() {
      return store.state.runMap;
    }
  }
};
</script>
<style>
</style>

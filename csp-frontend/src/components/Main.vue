<template>
    <div>
        <div class="container">
            <v-controls></v-controls>
            <main class="flex-grow-1">
                <router-view/>
            </main>
            <v-footer class="border-top mt-4">
                <template slot="content">
                    <div class="position-relative d-flex flex-justify-between">
                        <ul class="list-style-none d-flex flex-wrap ml-4 mt-3">
                            <li class="mr-3">© 2018 Nitxiodev</li>
                        </ul>
                        <a href="https://github.com/nitxiodev" target="_blank" class="mt-1 mr-4"><i class="fab fa-github fa-3x"></i></a>
                    </div>
                </template>
            </v-footer>
        </div>
    </div>
</template>
<script>
import Footer from "@/components/Footer.vue";
import Controls from "@/components/ControlsHeader.vue";
import Card from "@/components/BaseCard.vue";
import store from "../store";
export default {
  name: "Main",
  components: {
    "v-footer": Footer,
    "v-controls": Controls,
    "v-card": Card
  },
  sockets: {
    connect: function() {
      this.$socket.emit("my_id");
      console.log("socket connected");
    },
    connected: function(e) {
      console.log("CONECTADO ", e);
      store.commit("UPDATE_ME", e);
    }
  }
};
</script>
<style scoped>
.list-style-none {
  list-style-type: none !important;
}
.position-relative {
  position: relative !important;
}
.flex-justify-between {
  justify-content: space-between !important;
}
i {
  /*font-size: 25px;*/
  vertical-align: middle;
}
a:hover {
  color: red;
}
</style>

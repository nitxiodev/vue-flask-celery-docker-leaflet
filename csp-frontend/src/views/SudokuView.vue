<template>
  <div class="container">
    <Sudoku></Sudoku>
  </div>
</template>
<script>
import Sudoku from "@/components/Sudoku.vue";
import store from "../store";
import mixin from "../viewMixin";
export default {
  name: "sudoku",
  mixins: [mixin],
  components: {
    Sudoku
  },
  computed: {
    running: function() {
      return store.state.runSudoku;
    }
  }
};
</script>

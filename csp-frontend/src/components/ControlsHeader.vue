<template>
    <nav class="nav nav-pills nav-fill border-bottom p-2 mb-2">
        <router-link :class="{'custom-active': current === '/'}" class="nav-item nav-link default mr-1" to="/">Map</router-link>
        <router-link :class="{'custom-active': current === '/sudoku'}" class="nav-item nav-link default ml-1" to="/sudoku">Sudoku</router-link>
    </nav>
</template>
<script>
export default {
  name: "controlsHeader",
  computed: {
    current: function() {
      return this.$route.path;
    }
  }
};
</script>
<style scoped>
nav > a {
  color: black;
  font-weight: bold;
  text-transform: Capitalize;
}

nav > a:hover {
  background-color: #f6f6f6;
}

.default {
  border: none;
}

.custom-active {
  border: 1px solid gainsboro;
  -webkit-border-radius: 0 !important;
  -moz-border-radius: 0 !important;
  border-radius: 0 !important;
  background-color: transparent;
}
</style>

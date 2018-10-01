import Vue from "vue";
import Router from "vue-router";
// import Map from "./views/MapView.vue";
// import Sudoku from "./views/SudokuView.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "map",
      component: () =>
        import(/* webpackChunkName: "map" */ "./views/MapView.vue")
    },
    {
      path: "/sudoku",
      name: "sudoku", // eslint-disable-next-line
      component: () => import(/* webpackChunkName: "sudoku" */ "./views/SudokuView.vue")
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () =>
      //   import(/* webpackChunkName: "about" */ "./views/SudokuView.vue")
    },
    {
      path: "*",
      redirect: "/"
    }
  ]
});

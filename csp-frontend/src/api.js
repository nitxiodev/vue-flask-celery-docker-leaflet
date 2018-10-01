import Vue from "vue";
import store from "./store";

export default {
  sudoku: {
    solve: function(data) {
      return new Promise((resolve, reject) => {
        store.commit("UPDATE_SUDOKU", true);
        Vue.http
          .post("/sudoku_async", data)
          .then(response => {
            if (response.status === 201) {
              resolve(response.data);
            } else {
              store.commit("UPDATE_SUDOKU", false);
              reject(null);
            }
          })
          .catch(error => {
            store.commit("UPDATE_SUDOKU", false);
            reject(error);
          });
      });
    }
  },
  map: {
    location: function() {
      return new Promise((resolve, reject) => {
        Vue.http
          .get("http://ip-api.com/json")
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          });
      });
    },
    solve: function(data) {
      return new Promise((resolve, reject) => {
        store.commit("UPDATE_MAP", true);
        Vue.http
          .post("/map_async", data)
          .then(response => {
            if (response.status === 201) {
              resolve(response.data);
            } else {
              store.commit("UPDATE_MAP", false);
              reject(response.data);
            }
          })
          .catch(error => {
            store.commit("UPDATE_MAP", false);
            reject(error);
          });
      });
    },
    getData: function(task_id) {
      return new Promise((resolve, reject) => {
        Vue.http
          .get("/progress/" + task_id)
          .then(response => {
            if (response.status === 200) {
              let solution = response.data.msg;
              if (solution !== null) {
                resolve(JSON.parse(solution.solution));
              }
            }
            store.commit("UPDATE_MAP", false);
            reject(null);
          })
          .catch(error => {
            store.commit("UPDATE_MAP", false);
            reject(error);
          });
      });
    }
  }
};

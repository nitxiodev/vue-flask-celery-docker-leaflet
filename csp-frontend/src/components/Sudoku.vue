<template>
    <div>
        <v-card>
            <template slot="top">
                <form id="sudoku_solver" class="h-100" @submit.prevent="submitForm">
                    <table class="h-100">
                        <tbody>
                            <tr v-for="row in 9" :key="row">
                                <td v-for="col in 9" :key="col">
                                    <input @keydown.enter.prevent=""
                                           :class="{'setted': sudoku.inputs[((row-1)*(9))+(col-1)] > 0, 'text-danger': sudoku.inputs[((row-1)*(9))+(col-1)] < 0 || sudoku.inputs[((row-1)*(9))+(col-1)] > 9}"
                                           type="number" min="0" max="9" class="w-100" required
                                           v-model.number="sudoku.inputs[((row-1)*(9))+(col-1)]">
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </form>
            </template>
            <template slot="header">
                <span> Level: {{sudoku_level}}</span>
            </template>
            <template slot="body">
                <div class="row">
                    <div class="col-md-12">
                        <button @click="show(2)" @mouseenter="info(0)" @mouseleave="info(-1)" type="button" class="btn btn-default btn-circle mr-2"><i class="fas fa-upload"></i></button>
                        <button @click="show(0)" @mouseenter="info(1)" @mouseleave="info(-1)" type="button" class="btn btn-default btn-circle mr-2"><i class="fas fa-random"></i></button>
                        <button :disabled="sudoku.inputs.length == 0" @click="clean" @mouseenter="info(2)" @mouseleave="info(-1)" type="button" class="btn btn-danger btn-circle mr-2"><i class="fas fa-trash"></i></button>
                        <button :disabled="sudoku.inputs.length !== 81" @click="show(1)" @mouseenter="info(3)" @mouseleave="info(-1)" type="button" class="btn btn-default btn-circle mr-2"><i class="fas fa-download"></i></button>
                        <button type="submit" form="sudoku_solver" :disabled="sudoku.inputs.length !== 81 || !sudoku.inputs.every(x => typeof x === 'number')" @mouseenter="info(4)" @mouseleave="info(-1)" class="btn btn-success btn-circle"><i class="fas fa-long-arrow-alt-right"></i></button>
                    </div>
                </div>
                <v-overlay :show="overlay.show" :content="overlay.msg" :after="overlay.hide_after"></v-overlay>
            </template>
            <template slot="footer">
                {{buttonInfo}}
            </template>
        </v-card>
        <v-modal class="modal" ref="level" :centered="true">
            <template slot="header">
                <h5 class="font-weight-bold">Choose level</h5>
            </template>
            <template slot="body" slot-scope="{close}">
                <div class="row">
                    <div class="col-md-12 text-center">
                        <button @mouseenter="cur_difficulty=1" @mouseleave="cur_difficulty=-1" @click="random_sudoku(1); close()" type="button" class="btn btn-default btn-circle custom ultra-easy mr-2">E</button>
                        <button @mouseenter="cur_difficulty=2" @mouseleave="cur_difficulty=-1" @click="random_sudoku(2); close()" type="button" class="btn btn-default btn-circle custom easy mr-2">S</button>
                        <button @mouseenter="cur_difficulty=3" @mouseleave="cur_difficulty=-1" @click="random_sudoku(3); close()" type="button" class="btn btn-default btn-circle custom medium mr-2">M</button>
                        <button @mouseenter="cur_difficulty=4" @mouseleave="cur_difficulty=-1" @click="random_sudoku(4); close()" type="button" class="btn btn-default btn-circle custom hard mr-2">H</button>
                        <button @mouseenter="cur_difficulty=5" @mouseleave="cur_difficulty=-1" @click="random_sudoku(5); close()" type="button" class="btn btn-default btn-circle custom evil mr-2">V</button>
                        <button @mouseenter="cur_difficulty=6" @mouseleave="cur_difficulty=-1" @click="random_sudoku(6); close()" type="button" class="btn btn-default btn-circle custom insane mr-2">I</button>
                    </div>
                </div>
            </template>
            <template slot="footer">
                <div class="row">
                    <div class="col-md-12 font-weight-bold ">
                        <span v-if="cur_difficulty !== -1">{{parse_difficulty(cur_difficulty)}}</span>
                        <span v-else>-</span>
                    </div>
                </div>
            </template>
        </v-modal>
        <v-modal class="modal" ref="download" :centered="true">
            <template slot="header">
                <h5 class="font-weight-bold">Sudoku ({{parse_difficulty(sudoku.difficulty)}})</h5>
            </template>
            <template slot="body">
                <div class="row">
                    <div class="col-md-12 text-center">
                        <span class="wrap">"{{sudoku_as_string}}"</span>
                    </div>
                </div>
            </template>
        </v-modal>
        <v-modal class="modal" ref="upload" :centered="true">
            <template slot="header">
                <h5 class="font-weight-bold">Upload a Stringify Sudoku</h5>
            </template>
            <template slot="body">
                <div class="row">
                    <div class="col-md-12 text-center">
                        <input type="text" class="w-100 upload_sudoku" v-model="modals.sudoku_upload">
                    </div>
                </div>
            </template>
            <template slot="footer" slot-scope="{close}">
                <div class="row">
                    <div class="col-md-12 text-center ">
                        <button  :disabled="modals.sudoku_upload.length === 0"
                                @click="modals.sudoku_upload = ''" type="button" class="btn btn-danger btn-circle mr-2"><i class="fa fa-trash"></i></button>
                        <button :disabled="modals.sudoku_upload.length !== 81"
                                @click="upload(); close(); modals.sudoku_upload = ''" type="button" class="btn btn-success btn-circle"><i class="fa fa-check"></i></button>
                    </div>
                </div>
            </template>
        </v-modal>
    </div>
</template>

<script>
import Card from "./BaseCard.vue";
import Modal from "./Modal.vue";
import store from "../store";
import Overlay from "./Overlay.vue";
import { gen, download_sudoku, parse, level } from "../SudokuGenerator";
import api from "../api";
export default {
  name: "sudoku",
  components: {
    "v-card": Card,
    "v-modal": Modal,
    "v-overlay": Overlay
  },
  created: function() {
    this.$options.sockets.sudokuSol = sol => {
      if (store.state.runSudoku) {
        let solution = sol.solution;

        if (solution) {
          this.sudoku.inputs = parse(solution);
          this.hideOverlay();
        } else {
          let self = this;
          setTimeout(function() {
            self.showOverlay("No solution! :(", 2000);
          }, 100);
        }
        store.commit("UPDATE_SUDOKU", false);
      }
    };
  },
  data: function() {
    return {
      sudoku: {
        inputs: [],
        difficulty: -1
      },
      buttonInfo: "-",
      cur_difficulty: -1,
      modals: {
        sudoku_upload: ""
      },
      sudoku_as_string: "",
      overlay: {
        show: false,
        msg: "Loading",
        hide_after: 0
      }
    };
  },
  computed: {
    sudoku_level: function() {
      return this.parse_difficulty(this.sudoku.difficulty);
    },
    state: function() {
      return store.state.me;
    }
  },
  methods: {
    showOverlay: function(msg, hide_after) {
      this.overlay.msg = msg;
      this.overlay.hide_after = hide_after;
      this.overlay.show = hide_after > 0 ? !this.overlay.show : true;
    },
    hideOverlay: function() {
      this.overlay.show = false;
    },
    isSolved: function() {
      // We check if we have already the grid full
      return (
        this.sudoku.inputs.reduce(function(n, val) {
          return n + (val > 0);
        }, 0) === 81
      );
    },
    submitForm: function() {
      let data = {
        sudoku: this.sudoku.inputs,
        id: this.state
      };

      if (!this.isSolved()) {
        api.sudoku
          .solve(data)
          .then(() => {
            this.showOverlay("Loading!", 0);
          })
          .catch(error => {
            if (error === null) {
              this.showOverlay("No solution or error found! :(", 2000);
            } else {
              this.showOverlay("Ouch! Houston, we have a problem....", 500);
            }
          })
          .finally(() => {
            this.hideOverlay();
          });
      } else {
        this.showOverlay(
          "Sudoku board is full and could be already solved",
          500
        );
        console.log("SOLVED!");
      }
    },
    show: function(modal_id) {
      console.log(this.$refs);
      switch (modal_id) {
        case 0:
          this.$refs.level.show();
          break;
        case 1:
          this.download();
          this.$refs.download.show();
          break;
        case 2:
          this.$refs.upload.show();
          break;
        default:
          break;
      }
    },
    parse_difficulty: function(difficulty) {
      let _difficulty;
      switch (difficulty) {
        case 1:
          _difficulty = "Extremely Easy";
          break;
        case 2:
          _difficulty = "Easy";
          break;
        case 3:
          _difficulty = "Medium";
          break;
        case 4:
          _difficulty = "Hard";
          break;
        case 5:
          _difficulty = "Evil";
          break;
        case 6:
          _difficulty = "Insane";
          break;
        default:
          _difficulty = "-";
          break;
      }
      return _difficulty;
    },
    info: function(message_type) {
      switch (message_type) {
        case 0:
          this.buttonInfo = "Upload a sudoku from file";
          break;
        case 1:
          this.buttonInfo = "Generate a random sudoku";
          break;
        case 2:
          this.buttonInfo = "Clean the grid";
          break;
        case 3:
          this.buttonInfo = "Download sudoku as string";
          break;
        case 4:
          this.buttonInfo = "Send data to the server";
          break;
        default:
          this.buttonInfo = "-";
          break;
      }
    },
    clean: function() {
      this.sudoku.inputs = [];
      this.modals.sudoku_upload = "";
      this.sudoku.difficulty = -1;
    },
    random_sudoku: function(level) {
      this.sudoku.difficulty = level;
      this.fill_board(gen(this.sudoku.difficulty));
    },
    download: function() {
      this.sudoku_as_string = download_sudoku(this.sudoku.inputs);
    },
    fill_board: function(sudoku) {
      for (let i = 0; i < sudoku.length; i++) {
        this.$set(this.sudoku.inputs, i, sudoku[i]); // needed for reactivity!
      }
    },
    upload: function() {
      this.fill_board(parse(this.modals.sudoku_upload));
      console.log(level(this.sudoku.inputs));
      this.sudoku.difficulty = level(this.sudoku.inputs);
    }
  }
};
</script>
<style scoped>
input:focus {
  outline: none;
}
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
tr:nth-child(3n):not(:last-child) td {
  border-bottom: 2px solid black;
}
td {
  border: 1px solid lightgrey;
}
td:nth-child(3n):not(:last-child) {
  border-right: 2px solid black;
}
input:nth-child(even) {
  background-color: #f9f9f9;
}
input {
  padding: 0;
  text-align: center;
  border: 0;
  height: 100%;
  font-size: 50px;
}

input:hover {
  background: #eee;
}
.setted {
  background-color: #80808017;
  /*pointer-events: none;*/
}
.custom {
  font-size: 20px;
  font-weight: bold;
  background-color: #dadada;
}
.ultra-easy {
  background-color: #00f300;
  color: white;
}
.easy {
  background-color: #00c500;
  color: white;
}
.medium {
  background-color: #b6c500;
  color: white;
}
.hard {
  background-color: #d27600;
  color: white;
}
.evil {
  background-color: #d22e00;
  color: white;
}
.insane {
  background-color: #000000;
  color: white;
}
.custom-footer {
  justify-content: center !important;
}
.upload_sudoku {
  border: 1px solid gainsboro;
  font-size: 30px;
  background-color: #d3d3d33d;
}
.wrap {
  word-wrap: break-word;
}
</style>

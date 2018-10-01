<template>
    <div class="overlay text-center d-flex justify-content-center align-items-center" v-if="visible">
        <div class="container">
            <div class="row">
                <div class="col-md-12 text-center" v-show="after === 0">
                    <i class="fas fa-spinner fa-2x fa-spin" style="color: #00f300"></i>
                </div>
                <div class="col-md-12 text-center">
                    <span class="font-weight-bold">{{content}}</span>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
  name: "overlay",
  props: {
    show: {
      type: Boolean,
      default: true
    },
    hide_spinner: {
      type: Boolean,
      default: false
    },
    content: {
      type: String,
      default: "Loading"
    },
    after: {
      type: Number,
      default: 0
    }
  },
  data: function() {
    return {
      must_show: this.show
    };
  },
  computed: {
    visible: {
      get: function() {
        return this.must_show;
      },
      set: function(newVal) {
        this.must_show = newVal;
      }
    }
  },
  watch: {
    show: function(newValue, oldValue) {
      console.log(
        "OVERLAYCPM",
        newValue,
        oldValue,
        this.after,
        this.visible,
        this.content
      );
      this.visible = oldValue;
      if (this.after > 0) {
        this.visible = true;
        let when = this.after > 1000 ? this.after : 2000;
        this.hide_after(when);
      } else {
        this.visible = newValue;
      }
    }
  },
  methods: {
    hide_after: function(seconds) {
      let self = this;
      setTimeout(function() {
        self.visible = false;
      }, seconds);
    }
  }
};
</script>
<style scoped>
.overlay {
  position: absolute; /* Sit on top of the page content */
  width: 100%; /* Full width (cover the whole page) */
  height: 100%; /* Full height (cover the whole page) */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 1); /* Black background with opacity */
  z-index: 2; /* Specify a stack order in case you're using a different order for other elements */
  cursor: default; /* Add a pointer on hover */
}
</style>

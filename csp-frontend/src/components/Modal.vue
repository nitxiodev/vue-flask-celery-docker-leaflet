<template>
  <transition name="fade">
    <div class="modal modal-mask" v-show="!hide">
      <div class="modal-dialog" :class="{'modal-dialog-centered': centered}" role="document">
        <div class="modal-content">
          <div class="modal-header">
              <slot name="header"></slot>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close"
                      @click="close">
                <span aria-hidden="true" class="modal-button">&times;</span>
              </button>
          </div>

          <div class="modal-body">
            <slot name="body" :close="close"></slot>
          </div>

          <div class="modal-footer">
            <slot name="footer" :close="close"></slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "modal",
  props: {
    centered: {
      type: Boolean,
      default: false
    }
  },
  data: function() {
    return {
      hide: true
    };
  },
  methods: {
    show: function() {
      this.hide = false;
    },
    close: function() {
      this.hide = true;
    }
  }
};
</script>

<style scoped>
.modal-header > .row {
  padding-bottom: 25px;
}
.modal-header {
  border-bottom: thin solid #949ba2;
}
.modal-footer {
  border-top: thin solid #949ba2;
}
.modal-content {
  /*background-color: #2d3038;*/
}
.modal-title {
  color: orange;
}
.modal-mask {
  z-index: 9999;
  background-color: rgba(0, 0, 0, 0.5);
  display: block;
  transition: opacity 0.3s ease;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
.modal-footer {
  justify-content: center;
}
.close {
  color: #494949;
}
.close:focus {
  outline: none !important;
}
</style>

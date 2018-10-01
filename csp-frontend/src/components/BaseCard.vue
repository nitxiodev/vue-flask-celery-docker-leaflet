<template>
    <div class="w-100">
        <div class="col-md-12">
            <div class="card">
                <div class="card-img-top">
                    <slot name="top"></slot>
                </div>
                <div class="card-header text-center position-relative">
                    <slot name="header"></slot>
                </div>
                <div class="card-body text-center position-relative">
                    <slot name="body"></slot>
                </div>
                <div class="card-footer text-muted text-center position-relative">
                    <slot name="footer"></slot>
                </div>
            </div>
        </div>
    </div>
</template>
<style scoped>
.card-img-top {
  height: 700px;
}
.card {
  border: 2px solid black;
}
.card-header {
  border-top: 2px solid black;
}
</style>

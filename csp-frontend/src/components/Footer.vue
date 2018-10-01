<template>
    <footer class="footer mt-2">
        <div class="">
            <slot name="content"></slot>
        </div>
    </footer>
</template>

<style scoped>
.footer {
  /*position: inherit;*/
  text-align: center;
  font-size: 14px;
}
a {
  color: black;
}
</style>

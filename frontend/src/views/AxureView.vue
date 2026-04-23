<template>
  <iframe class="axure-iframe" :src="src" />
</template>

<script setup>
defineProps({
  src: { type: String, required: true },
});
</script>

<style scoped>
.axure-iframe {
  width: 100vw;
  height: 100vh;
  border: 0;
  display: block;
}
</style>


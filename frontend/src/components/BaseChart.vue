<template>
  <div ref="chartRef" :style="{ width: width, height: height }"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, markRaw } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
  option: { type: Object, required: true },
  width: { type: String, default: '100%' },
  height: { type: String, default: '300px' }
});

const chartRef = ref(null);
const chartInstance = ref(null);

onMounted(() => {
  chartInstance.value = markRaw(echarts.init(chartRef.value));
  chartInstance.value.setOption(props.option);
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  if (chartInstance.value) chartInstance.value.dispose();
});

watch(() => props.option, (newOption) => {
  if (chartInstance.value) chartInstance.value.setOption(newOption);
}, { deep: true });

function handleResize() {
  if (chartInstance.value) chartInstance.value.resize();
}
</script>
<template>
  <div class="page-card">
    <h2>用电分析</h2>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>峰平谷结构</template>
          <BaseChart v-if="pieOption" :option="pieOption" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>用电统计</template>
          <div v-if="data" style="font-size: 18px; line-height: 2;">
            <p>总用电量：{{ data.total_power }} kWh</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import request from '../utils/request';
import BaseChart from '../components/BaseChart.vue';

const data = ref(null);
const pieOption = ref(null);

onMounted(async () => {
  const res = await request.get('/analytics/power/');
  data.value = res.data || res;
  const payload = res.data || res;
  
  pieOption.value = {
    tooltip: { trigger: 'item' },
    legend: { top: 'bottom' },
    series: [
      {
        name: '用电量',
        type: 'pie',
        radius: '50%',
        data: payload.peak_valley,
        emphasis: {
          itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' }
        }
      }
    ]
  };
});
</script>
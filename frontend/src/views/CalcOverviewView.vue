<template>
  <div class="page-card">
    <h2>能碳总览</h2>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>碳排放趋势</template>
          <BaseChart v-if="chartOption" :option="chartOption" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>核心指标</template>
          <div v-if="data" style="font-size: 18px; line-height: 2;">
            <p>总碳排放：{{ data.total_carbon }} tCO2e</p>
            <p>总能耗：{{ data.total_energy }} tce</p>
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
const chartOption = ref(null);

onMounted(async () => {
  const res = await request.get('/analytics/overview/');
  data.value = res.data || res;
  
  const payload = res.data || res;
  chartOption.value = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: payload.trend_data.months },
    yAxis: { type: 'value' },
    series: [
      { name: '碳排放', type: 'line', data: payload.trend_data.carbon },
      { name: '能耗', type: 'bar', data: payload.trend_data.energy }
    ]
  };
});
</script>
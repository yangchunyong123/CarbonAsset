<template>
  <div class="dashboard-container">
    <el-row :gutter="20" style="height: 100%;">
      <!-- 左侧个人/企业信息卡片及快捷入口 -->
      <el-col :span="6">
        <div class="left-panel">
          <!-- 用户信息卡片 -->
          <div class="user-card">
            <div class="avatar-container">
              <el-avatar :size="80" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
            </div>
            <h3 class="company-name">杭州零碳领跑者科技有限公司</h3>
            <div class="metrics-row">
              <div class="metric-item">
                <div class="metric-value">10,4562</div>
                <div class="metric-label">碳排放额度</div>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 60%;"></div>
                </div>
                <div class="progress-text">60%</div>
              </div>
              <div class="metric-item">
                <div class="metric-value">98.34</div>
                <div class="metric-label">碳效评分</div>
                <div class="metric-trend text-success">
                  同比12% <el-icon><Top /></el-icon>
                </div>
              </div>
            </div>
            <div class="ranking-bar">
              <span class="industry-tag">纺织行业</span>
              <span class="ranking-text">当前同行业排名：<span class="ranking-num">18</span></span>
            </div>
          </div>

          <!-- 快捷入口网格 -->
          <div class="shortcut-grid">
            <div class="shortcut-item">
              <div class="shortcut-icon"><el-icon><EditPen /></el-icon></div>
              <span>碳核算填报</span>
            </div>
            <div class="shortcut-item">
              <div class="shortcut-icon"><el-icon><Document /></el-icon></div>
              <span>碳排放报告</span>
            </div>
            <div class="shortcut-item">
              <div class="shortcut-icon"><el-icon><Search /></el-icon></div>
              <span>碳排放查询</span>
            </div>
            <div class="shortcut-item">
              <div class="shortcut-icon"><el-icon><TrendCharts /></el-icon></div>
              <span>碳排放分析</span>
            </div>
            <div class="shortcut-item">
              <div class="shortcut-icon"><el-icon><Warning /></el-icon></div>
              <span>碳排放预警</span>
            </div>
            <div class="shortcut-item">
              <div class="shortcut-icon"><el-icon><DataLine /></el-icon></div>
              <span>碳额度配置</span>
            </div>
            <div class="shortcut-item">
              <div class="shortcut-icon"><el-icon><Connection /></el-icon></div>
              <span>碳模型配置</span>
            </div>
            <div class="shortcut-item">
              <div class="shortcut-icon"><el-icon><Setting /></el-icon></div>
              <span>碳核算配置</span>
            </div>
          </div>
        </div>
      </el-col>

      <!-- 中间核心数据与图表 -->
      <el-col :span="12">
        <div class="center-panel">
          <!-- 顶部提示消息 -->
          <el-alert
            title="本月用能情况基本符合去年的趋势，同比增长百分之3.8。"
            type="primary"
            show-icon
            :closable="true"
            class="trend-alert"
          >
            <template #title>
              <span style="margin-right: 10px;">本月用能情况基本符合去年的趋势，同比增长百分之3.8。</span>
              <el-link type="primary" :underline="false">查看详情</el-link>
            </template>
          </el-alert>

          <!-- 碳排放总览数据卡片 -->
          <div class="section-title">
            <div class="title-indicator"></div>
            碳排放总览
          </div>
          <el-row :gutter="20" class="overview-cards">
            <el-col :span="6" v-for="(item, index) in overviewData" :key="index">
              <div class="overview-item">
                <div class="overview-value-row">
                  <span class="overview-value" :style="{ color: item.color }">{{ item.value }}</span>
                  <span :class="['overview-trend', item.trend > 0 ? 'text-success' : 'text-danger']">
                    {{ Math.abs(item.trend) }}% 
                    <el-icon><Top v-if="item.trend > 0" /><Bottom v-else /></el-icon>
                  </span>
                </div>
                <div class="overview-label">{{ item.label }}</div>
              </div>
            </el-col>
          </el-row>

          <!-- 碳排放趋势图 -->
          <div class="section-title">
            <div class="title-indicator"></div>
            碳排放趋势
          </div>
          <div class="chart-container">
            <BaseChart v-if="trendChartOption" :option="trendChartOption" height="280px" />
          </div>

          <!-- 能源消耗结构图 -->
          <div class="section-title">
            <div class="title-indicator"></div>
            能源消耗结构
          </div>
          <div class="structure-charts">
            <BaseChart v-if="structureChartOption1" :option="structureChartOption1" width="25%" height="150px" />
            <BaseChart v-if="structureChartOption2" :option="structureChartOption2" width="25%" height="150px" />
            <BaseChart v-if="structureChartOption3" :option="structureChartOption3" width="25%" height="150px" />
            <BaseChart v-if="structureChartOption4" :option="structureChartOption4" width="25%" height="150px" />
          </div>
        </div>
      </el-col>

      <!-- 右侧日历与提醒事项 -->
      <el-col :span="6">
        <div class="right-panel">
          <div class="calendar-header">
            <h3>2020年04月</h3>
            <div class="calendar-nav">
              <el-icon><ArrowLeft /></el-icon>
              <el-icon><ArrowRight /></el-icon>
            </div>
          </div>
          
          <el-calendar class="custom-calendar" v-model="calendarValue" />
          
          <div class="today-info">
            <div class="today-date">17</div>
            <div class="today-details">
              <div>星期五</div>
              <div class="lunar-date">五月初九 壬寅年 虎 丙午月 辛卯日</div>
            </div>
            <el-button type="primary" circle class="add-btn">
              <el-icon><Plus /></el-icon>
            </el-button>
          </div>

          <div class="reminders-list">
            <div class="reminder-item" v-for="(item, index) in reminders" :key="index">
              <el-tag size="small" type="info" class="reminder-tag">提醒</el-tag>
              <span class="reminder-content">{{ item.content }}</span>
              <span class="reminder-time text-success">{{ item.time }}</span>
            </div>
          </div>
          
          <div class="view-more">
            <el-link type="primary" :underline="false">查看更多提醒...</el-link>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { 
  Top, Bottom, EditPen, Document, Search, TrendCharts, 
  Warning, DataLine, Connection, Setting, ArrowLeft, ArrowRight, Plus 
} from '@element-plus/icons-vue';
import BaseChart from '../components/BaseChart.vue';

const calendarValue = ref(new Date('2020-04-17'));

const overviewData = ref([
  { label: '能源消费总量 (吨标煤)', value: '5421.45', trend: 12, color: '#1890ff' },
  { label: '碳排放总量 (吨CO₂)', value: '3654.19', trend: -12, color: '#1890ff' },
  { label: '能耗强度 (吨标煤/万元)', value: '2.45', trend: 12, color: '#1890ff' },
  { label: '碳排放强度 (吨CO₂/万元)', value: '0.26', trend: 12, color: '#1890ff' },
]);

const reminders = ref([
  { content: '产品主线排放因子及指标数据库设计讨论', time: '17:45' },
  { content: '现有项目研发资源确认', time: '15:15' },
  { content: '5月能耗用量填报工作已开始，请尽快填写', time: '15:15' },
]);

const trendChartOption = ref(null);
const structureChartOption1 = ref(null);
const structureChartOption2 = ref(null);
const structureChartOption3 = ref(null);
const structureChartOption4 = ref(null);

onMounted(() => {
  // 趋势图配置
  trendChartOption.value = {
    grid: { left: '3%', right: '4%', bottom: '3%', top: '10%', containLabel: true },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['1990', '1994', '1998', '2002', '2006', '2010', '2014', '2018'],
      axisLine: { show: false },
      axisTick: { show: false }
    },
    yAxis: {
      type: 'value',
      name: '单位：(tCO₂)',
      nameTextStyle: { color: '#999', align: 'right' },
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { type: 'dashed', color: '#eee' } }
    },
    series: [
      {
        name: '碳排放总量',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        itemStyle: { color: '#1890ff' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(24,144,255,0.2)' },
              { offset: 1, color: 'rgba(24,144,255,0)' }
            ]
          }
        },
        data: [600, 500, 320, 720, 630, 600, 1050, 780]
      }
    ]
  };

  // 环形图生成函数
  const createRingOption = (name, value, color) => ({
    title: {
      text: `${value}%`,
      left: 'center',
      top: '35%',
      textStyle: { fontSize: 18, color: '#333', fontWeight: 'normal' }
    },
    series: [
      {
        type: 'pie',
        radius: ['60%', '75%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: false,
        label: { show: false },
        data: [
          { value: value, itemStyle: { color: color } },
          { value: 100 - value, itemStyle: { color: '#f0f2f5' } }
        ]
      }
    ],
    graphic: {
      type: 'text',
      left: 'center',
      bottom: '0',
      style: { text: name, fill: '#666', font: '13px sans-serif' }
    }
  });

  structureChartOption1.value = createRingOption('煤: 452.4 (吨标煤)', 48, '#1890ff');
  structureChartOption2.value = createRingOption('气: 152.1 (吨标煤)', 31, '#722ed1');
  structureChartOption3.value = createRingOption('油: 23.43 (吨标煤)', 6, '#13c2c2');
  structureChartOption4.value = createRingOption('电: 89.21 (吨标煤)', 15, '#fa8c16');
});
</script>

<style scoped>
.dashboard-container {
  padding: 0;
  background-color: #f0f2f5;
  min-height: calc(100vh - 60px);
}

.text-success { color: #52c41a; }
.text-danger { color: #f5222d; }

/* 左侧面板 */
.left-panel {
  background: #fff;
  height: 100%;
  border-radius: 4px;
  overflow: hidden;
}

.user-card {
  background-color: #001529;
  color: #fff;
  padding: 40px 20px 20px;
  text-align: center;
  position: relative;
}

.avatar-container {
  margin-bottom: 20px;
}

.company-name {
  font-size: 16px;
  font-weight: normal;
  margin-bottom: 30px;
}

.metrics-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  text-align: left;
}

.metric-item {
  flex: 1;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 8px;
}

.metric-label {
  font-size: 12px;
  color: rgba(255,255,255,0.65);
  margin-bottom: 8px;
}

.progress-bar {
  height: 4px;
  background: rgba(255,255,255,0.2);
  border-radius: 2px;
  width: 80%;
  margin-bottom: 4px;
}

.progress-fill {
  height: 100%;
  background: #1890ff;
  border-radius: 2px;
}

.progress-text {
  font-size: 12px;
  color: rgba(255,255,255,0.85);
}

.metric-trend {
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.ranking-bar {
  background: #fffbe6;
  color: #fa8c16;
  margin: 0 -20px -20px;
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.industry-tag {
  color: #333;
  font-weight: bold;
}

.ranking-num {
  font-size: 20px;
  font-weight: bold;
}

.shortcut-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1px;
  background: #f0f2f5;
  padding: 20px;
}

.shortcut-item {
  background: #fff;
  padding: 30px 10px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.shortcut-item:hover {
  background: #f8faff;
}

.shortcut-icon {
  font-size: 32px;
  color: #1890ff;
  margin-bottom: 12px;
}

/* 中间面板 */
.center-panel {
  background: #fff;
  height: 100%;
  padding: 20px;
  border-radius: 4px;
}

.trend-alert {
  margin-bottom: 24px;
  background-color: #e6f7ff;
  color: #1890ff;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.title-indicator {
  width: 4px;
  height: 16px;
  background: #1890ff;
  margin-right: 8px;
}

.overview-cards {
  margin-bottom: 30px;
}

.overview-item {
  padding: 10px 0;
}

.overview-value-row {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 8px;
}

.overview-value {
  font-size: 28px;
  font-weight: bold;
}

.overview-trend {
  font-size: 12px;
  display: flex;
  align-items: center;
}

.overview-label {
  font-size: 13px;
  color: #666;
}

.chart-container {
  margin-bottom: 30px;
}

.structure-charts {
  display: flex;
  justify-content: space-between;
}

/* 右侧面板 */
.right-panel {
  background: #fff;
  height: 100%;
  padding: 20px;
  border-radius: 4px;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.calendar-header h3 {
  margin: 0;
  font-size: 18px;
}

.calendar-nav {
  display: flex;
  gap: 10px;
  color: #1890ff;
  cursor: pointer;
}

/* 覆盖 Element Plus 日历默认样式 */
:deep(.el-calendar-table .el-calendar-day) {
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

:deep(.el-calendar__header) {
  display: none; /* 隐藏自带头部 */
}

.today-info {
  display: flex;
  align-items: center;
  padding: 20px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
  margin: 10px 0 20px;
  position: relative;
}

.today-date {
  font-size: 40px;
  margin-right: 15px;
}

.today-details {
  font-size: 13px;
  color: #333;
}

.lunar-date {
  color: #999;
  margin-top: 4px;
}

.add-btn {
  position: absolute;
  right: 0;
  background: #13c2c2;
  border-color: #13c2c2;
}

.reminders-list {
  margin-bottom: 20px;
}

.reminder-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px dashed #f0f0f0;
}

.reminder-tag {
  margin-right: 10px;
  border-radius: 2px;
}

.reminder-content {
  flex: 1;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 10px;
}

.reminder-time {
  font-size: 13px;
  font-weight: bold;
}

.view-more {
  text-align: right;
}
</style>
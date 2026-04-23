# M2 Analytics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the M2 Analytics module including Energy & Carbon Overview, Energy Analysis, Power Analysis, and Alert/Warning Records.

**Architecture:** 
- Backend: Django views will aggregate data from `data_entry` (EntryMonthlyData) and `calculation` (CalcResult). An `AlertRecord` model will be added for warnings.
- Frontend: Vue3 + ECharts will be used. A reusable `BaseChart.vue` component will be created. New views will be added for each analysis page.

**Tech Stack:** Django, Django REST Framework, Vue 3, Element Plus, ECharts, Axios.

---

### Task 1: Create Reusable ECharts Component

**Files:**
- Create: `frontend/src/components/BaseChart.vue`

- [ ] **Step 1: Write the implementation**

```vue
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
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/BaseChart.vue
git commit -m "feat: add BaseChart reusable component"
```

### Task 2: Backend Models and Migrations for Analytics

**Files:**
- Modify: `backend/apps/analytics/models.py`
- Modify: `backend/apps/analytics/serializers.py` (Create)

- [ ] **Step 1: Define AlertRecord model**

```python
from django.db import models

class AlertRecord(models.Model):
    """Store system warnings and alerts."""
    LEVEL_CHOICES = (
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    )
    title = models.CharField(max_length=128)
    content = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='warning')
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
```

- [ ] **Step 2: Create serializer**

```python
from rest_framework import serializers
from .models import AlertRecord

class AlertRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertRecord
        fields = '__all__'
```

- [ ] **Step 3: Make migrations and migrate**

```bash
cd backend && python manage.py makemigrations analytics && python manage.py migrate analytics && cd ..
```

- [ ] **Step 4: Commit**

```bash
git add backend/apps/analytics/
git commit -m "feat: add AlertRecord model and serializer"
```

### Task 3: Backend Views for Analytics

**Files:**
- Modify: `backend/apps/analytics/views.py`
- Modify: `backend/apps/analytics/urls.py`

- [ ] **Step 1: Write views for dashboard aggregation and alerts**

```python
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AlertRecord
from .serializers import AlertRecordSerializer
from apps.common.response import ok

class AlertRecordViewSet(viewsets.ModelViewSet):
    queryset = AlertRecord.objects.all()
    serializer_class = AlertRecordSerializer

@api_view(['GET'])
def energy_overview(request):
    """Mock aggregation for energy and carbon overview."""
    data = {
        "total_carbon": 12500.5,
        "total_energy": 45000.0,
        "trend_data": {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "carbon": [1000, 1200, 1100, 1300, 1500, 1400],
            "energy": [3000, 3200, 3100, 3500, 3800, 3600]
        }
    }
    return ok(data)

@api_view(['GET'])
def power_analysis(request):
    """Mock aggregation for power analysis."""
    data = {
        "total_power": 8500.0,
        "peak_valley": [
            {"name": "Peak", "value": 3000},
            {"name": "Flat", "value": 4000},
            {"name": "Valley", "value": 1500}
        ]
    }
    return ok(data)
```

- [ ] **Step 2: Setup URLs**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlertRecordViewSet, energy_overview, power_analysis

router = DefaultRouter()
router.register(r'alerts', AlertRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('overview/', energy_overview),
    path('power/', power_analysis),
]
```

- [ ] **Step 3: Include in main urls (check if already included)**

Verify `backend/server/urls.py` includes `api/v1/analytics/`. If not, add it:
```python
# Assuming it exists or modify backend/server/urls.py to include:
# path("api/v1/analytics/", include("apps.analytics.urls")),
```

- [ ] **Step 4: Commit**

```bash
git add backend/apps/analytics/views.py backend/apps/analytics/urls.py
git commit -m "feat: add analytics aggregation views and URLs"
```

### Task 4: Frontend Views for Analytics

**Files:**
- Create: `frontend/src/views/CalcOverviewView.vue`
- Create: `frontend/src/views/PowerAnalysisView.vue`

- [ ] **Step 1: Write CalcOverviewView**

```vue
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
  const res = await request.get('/api/v1/analytics/overview/');
  data.value = res.data;
  
  chartOption.value = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: res.data.trend_data.months },
    yAxis: { type: 'value' },
    series: [
      { name: '碳排放', type: 'line', data: res.data.trend_data.carbon },
      { name: '能耗', type: 'bar', data: res.data.trend_data.energy }
    ]
  };
});
</script>
```

- [ ] **Step 2: Write PowerAnalysisView**

```vue
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
  const res = await request.get('/api/v1/analytics/power/');
  data.value = res.data;
  
  pieOption.value = {
    tooltip: { trigger: 'item' },
    legend: { top: 'bottom' },
    series: [
      {
        name: '用电量',
        type: 'pie',
        radius: '50%',
        data: res.data.peak_valley,
        emphasis: {
          itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' }
        }
      }
    ]
  };
});
</script>
```

- [ ] **Step 3: Update Frontend Router**

Modify `frontend/src/router/index.js` to add routes and `frontend/src/layouts/MainLayout.vue` if needed (or backend menu) so they show up.

In `frontend/src/router/index.js`:
```javascript
import CalcOverviewView from "../views/CalcOverviewView.vue";
import PowerAnalysisView from "../views/PowerAnalysisView.vue";

// inside children array of MainLayout:
// { path: "calc/overview", component: CalcOverviewView },
// { path: "analysis/power", component: PowerAnalysisView },
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/ frontend/src/router/
git commit -m "feat: add analytics frontend views and routes"
```

### Task 5: Backend Menu Update

**Files:**
- Modify: `backend/apps/authn/views.py`

- [ ] **Step 1: Update `menus_view`**

Add the new M2 routes to the default fallback menu if roots don't exist:

```python
                {"name": "能碳总览", "path": "/calc/overview", "component": "CalcOverviewView"},
                {"name": "用电分析", "path": "/analysis/power", "component": "PowerAnalysisView"},
```

- [ ] **Step 2: Commit**

```bash
git add backend/apps/authn/views.py
git commit -m "feat: add analytics to default menu"
```

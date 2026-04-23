<template>
  <div class="page-card">
    <CrudPage title="数据填报" endpoint="/data-entry/entries" :columns="columns" />
    <div style="margin-top: 16px">
      <el-input v-model="entryId" placeholder="输入填报ID进行计算" style="width: 220px; margin-right: 12px" />
      <el-button type="primary" @click="runCalc">执行计算</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";
import request from "../utils/request";
import CrudPage from "../components/CrudPage.vue";

const entryId = ref("");
const columns = [
  { prop: "year", label: "年份" },
  { prop: "month", label: "月份" },
  { prop: "org_name", label: "组织" },
  { prop: "status", label: "状态" },
];

/**
 * Trigger backend calculation task for the selected entry.
 */
async function runCalc() {
  if (!entryId.value) {
    ElMessage.warning("请先输入填报ID");
    return;
  }
  await request.post("/calculation/tasks/run/", { entry_id: Number(entryId.value) });
  ElMessage.success("计算任务执行完成");
}
</script>

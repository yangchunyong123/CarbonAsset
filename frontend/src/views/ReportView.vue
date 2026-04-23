<template>
  <CrudPage title="报告管理" endpoint="/reports/records" :columns="columns" />
</template>

<script setup>
import CrudPage from "../components/CrudPage.vue";

const columns = [
  { prop: "name", label: "报告名称" },
  { prop: "report_type", label: "报告类型" },
  { prop: "year", label: "年份" },
  { prop: "month", label: "月份" },
];
</script>

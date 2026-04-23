<template>
  <CrudPage title="核算配置模板" endpoint="/calc-config/templates" :columns="columns" />
</template>

<script setup>
import CrudPage from "../components/CrudPage.vue";

const columns = [
  { prop: "name", label: "模板名称" },
  { prop: "industry", label: "行业" },
  { prop: "version", label: "版本" },
  { prop: "is_active", label: "启用状态" },
];
</script>

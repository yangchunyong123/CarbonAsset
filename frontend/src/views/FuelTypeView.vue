<template>
  <CrudPage title="燃料品种管理" endpoint="/master-data/fuels" :columns="columns" />
</template>

<script setup>
import CrudPage from "../components/CrudPage.vue";

const columns = [
  { prop: "name", label: "名称" },
  { prop: "category", label: "类型" },
  { prop: "form", label: "形态" },
  { prop: "emission_factor", label: "排放因子" },
];
</script>

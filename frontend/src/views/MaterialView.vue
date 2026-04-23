<template>
  <CrudPage title="生产用料管理" endpoint="/master-data/materials" :columns="columns" />
</template>

<script setup>
import CrudPage from "../components/CrudPage.vue";

const columns = [
  { prop: "name", label: "名称" },
  { prop: "process_link", label: "关联环节" },
  { prop: "emission_factor", label: "排放因子" },
];
</script>

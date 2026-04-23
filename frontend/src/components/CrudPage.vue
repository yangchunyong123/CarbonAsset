<template>
  <div class="page-card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px">
      <h3 style="margin: 0">{{ title }}</h3>
      <el-button type="primary" @click="openCreate">新增</el-button>
    </div>
    <el-table :data="rows" border>
      <el-table-column v-for="col in columns" :key="col.prop" :prop="col.prop" :label="col.label" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button link type="primary" @click="openEdit(row)">编辑</el-button>
          <el-button link type="danger" @click="removeRow(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      style="margin-top: 12px"
      background
      layout="total, prev, pager, next"
      :total="total"
      :page-size="query.page_size"
      @current-change="onPageChange"
    />
    <el-dialog v-model="visible" :title="editingId ? '编辑' : '新增'" width="560px">
      <el-form :model="form" label-width="100px">
        <el-form-item v-for="col in editableColumns" :key="col.prop" :label="col.label">
          <el-input v-model="form[col.prop]" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch } from "vue";
import { ElNotification, ElMessageBox } from "element-plus";
import request from "../utils/request";

const props = defineProps({
  title: { type: String, required: true },
  endpoint: { type: String, required: true },
  columns: { type: Array, default: () => [] },
});

const rows = ref([]);
const total = ref(0);
const visible = ref(false);
const editingId = ref(null);
const form = reactive({});
const query = reactive({ page: 1, page_size: 20 });
const editableColumns = computed(() => props.columns.filter((c) => c.prop !== "id"));

/**
 * Request paginated data from target endpoint.
 */
async function loadData() {
  const res = await request.get(props.endpoint, { params: query });
  rows.value = res.data.results || res.data.list || [];
  total.value = res.data.count || res.data.total || 0;
}

/**
 * Open dialog for creating a new row.
 */
function openCreate() {
  editingId.value = null;
  Object.keys(form).forEach((k) => delete form[k]);
  visible.value = true;
}

/**
 * Open dialog and copy selected row into form model.
 */
function openEdit(row) {
  editingId.value = row.id;
  Object.keys(form).forEach((k) => delete form[k]);
  editableColumns.value.forEach((col) => {
    form[col.prop] = row[col.prop];
  });
  visible.value = true;
}

/**
 * Persist create or update action to backend endpoint.
 */
async function save() {
  if (editingId.value) {
    await request.put(`${props.endpoint}/${editingId.value}/`, form);
    ElNotification({ title: "成功", message: "更新成功", type: "success" });
  } else {
    await request.post(`${props.endpoint}/`, form);
    ElNotification({ title: "成功", message: "新增成功", type: "success" });
  }
  visible.value = false;
  await loadData();
}

/**
 * Confirm and remove a row by primary key.
 */
async function removeRow(id) {
  await ElMessageBox.confirm("确认删除该记录？", "提示", { type: "warning" });
  await request.delete(`${props.endpoint}/${id}/`);
  ElNotification({ title: "成功", message: "删除成功", type: "success" });
  await loadData();
}

/**
 * Handle pagination page change event.
 */
function onPageChange(page) {
  query.page = page;
  loadData();
}

watch(
  () => props.endpoint,
  () => {
    query.page = 1;
    loadData();
  },
  { immediate: true }
);
</script>

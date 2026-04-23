from pathlib import Path


def build_files():
    """Build frontend file map for M1 pages and infrastructure."""
    files = {}
    files["src/main.js"] = """import { createApp } from "vue";
import { createPinia } from "pinia";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import App from "./App.vue";
import router from "./router";
import "./style.css";

/**
 * Bootstrap and mount the Vue application.
 */
function bootstrap() {
  const app = createApp(App);
  app.use(createPinia());
  app.use(router);
  app.use(ElementPlus);
  app.mount("#app");
}

bootstrap();
"""
    files["src/App.vue"] = """<template>
  <router-view />
</template>
"""
    files["src/style.css"] = """* { box-sizing: border-box; }
body { margin: 0; background: #f5f7fa; font-family: "PingFang SC", "Microsoft Yahei", sans-serif; }
a { color: inherit; text-decoration: none; }
.page-card { background: #fff; padding: 16px; border-radius: 8px; }
"""
    files["src/utils/request.js"] = """import axios from "axios";
import { useAuthStore } from "../stores/auth";

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1",
  timeout: 15000,
});

/**
 * Attach JWT token to every outbound request when available.
 */
request.interceptors.request.use((config) => {
  const store = useAuthStore();
  if (store.accessToken) {
    config.headers.Authorization = `Bearer ${store.accessToken}`;
  }
  return config;
});

/**
 * Normalize API response and handle token expiration centrally.
 */
request.interceptors.response.use(
  (response) => response.data,
  async (error) => {
    const store = useAuthStore();
    if (error?.response?.status === 401) {
      store.logout();
      location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default request;
"""
    files["src/stores/auth.js"] = """import { defineStore } from "pinia";
import request from "../utils/request";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: localStorage.getItem("access_token") || "",
    refreshToken: localStorage.getItem("refresh_token") || "",
    user: JSON.parse(localStorage.getItem("user") || "null"),
  }),
  actions: {
    /**
     * Execute username/password login flow and persist session.
     */
    async login(payload) {
      const res = await request.post("/auth/login", payload);
      this.accessToken = res.data.tokens.access;
      this.refreshToken = res.data.tokens.refresh;
      this.user = res.data.user;
      localStorage.setItem("access_token", this.accessToken);
      localStorage.setItem("refresh_token", this.refreshToken);
      localStorage.setItem("user", JSON.stringify(this.user));
    },
    /**
     * Clear local session and reset store state.
     */
    logout() {
      this.accessToken = "";
      this.refreshToken = "";
      this.user = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user");
    },
  },
});
"""
    files["src/router/index.js"] = """import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
import LoginView from "../views/LoginView.vue";
import MainLayout from "../layouts/MainLayout.vue";
import DashboardView from "../views/DashboardView.vue";
import FuelTypeView from "../views/FuelTypeView.vue";
import MaterialView from "../views/MaterialView.vue";
import CalcTemplateView from "../views/CalcTemplateView.vue";
import DataEntryView from "../views/DataEntryView.vue";
import ReportView from "../views/ReportView.vue";

const routes = [
  { path: "/login", component: LoginView, meta: { public: true } },
  {
    path: "/",
    component: MainLayout,
    children: [
      { path: "", redirect: "/dashboard" },
      { path: "dashboard", component: DashboardView },
      { path: "master/fuels", component: FuelTypeView },
      { path: "master/materials", component: MaterialView },
      { path: "calc/templates", component: CalcTemplateView },
      { path: "calc/entries", component: DataEntryView },
      { path: "calc/reports", component: ReportView },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

/**
 * Guard routes and redirect unauthenticated users to login page.
 */
router.beforeEach((to) => {
  const store = useAuthStore();
  if (to.meta.public) return true;
  if (!store.accessToken) return "/login";
  return true;
});

export default router;
"""
    files["src/layouts/MainLayout.vue"] = """<template>
  <el-container style="height: 100vh">
    <el-aside width="220px" style="background: #001529; color: #fff">
      <div style="padding: 16px; font-weight: 700">碳资产管理系统V2</div>
      <el-menu :default-active="activePath" router background-color="#001529" text-color="#fff">
        <el-menu-item index="/dashboard">仪表盘</el-menu-item>
        <el-menu-item index="/master/fuels">燃料品种管理</el-menu-item>
        <el-menu-item index="/master/materials">生产用料管理</el-menu-item>
        <el-menu-item index="/calc/templates">核算配置</el-menu-item>
        <el-menu-item index="/calc/entries">数据填报</el-menu-item>
        <el-menu-item index="/calc/reports">报告管理</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="background: #fff; display: flex; justify-content: space-between; align-items: center">
        <div>M1 开发版本</div>
        <div>
          <span style="margin-right: 12px">{{ auth.user?.username || "未登录" }}</span>
          <el-button size="small" @click="onLogout">退出</el-button>
        </div>
      </el-header>
      <el-main><router-view /></el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();
const activePath = computed(() => route.path);

/**
 * Handle user logout and navigate back to login page.
 */
function onLogout() {
  auth.logout();
  router.push("/login");
}
</script>
"""
    files["src/views/LoginView.vue"] = """<template>
  <div style="height: 100vh; display: flex; justify-content: center; align-items: center; background: #f0f2f5">
    <el-card style="width: 420px">
      <template #header><div style="font-size: 18px; font-weight: 700">企业碳资产管理平台</div></template>
      <el-form :model="form" @submit.prevent>
        <el-form-item label="用户名">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password />
        </el-form-item>
        <el-button type="primary" :loading="loading" style="width: 100%" @click="onLogin">登录</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const auth = useAuthStore();
const loading = ref(false);
const form = reactive({ username: "admin", password: "Admin@123456" });

/**
 * Submit credentials and redirect to dashboard on success.
 */
async function onLogin() {
  loading.value = true;
  try {
    await auth.login(form);
    ElMessage.success("登录成功");
    router.push("/dashboard");
  } catch (error) {
    ElMessage.error("登录失败，请检查用户名或密码");
  } finally {
    loading.value = false;
  }
}
</script>
"""
    files["src/views/DashboardView.vue"] = """<template>
  <div class="page-card">
    <h3>欢迎使用 M1 版本</h3>
    <p>当前已交付：登录鉴权、主数据 CRUD、核算配置、数据填报、计算任务、报告管理。</p>
  </div>
</template>
"""
    files["src/views/FuelTypeView.vue"] = """<template>
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
"""
    files["src/views/MaterialView.vue"] = """<template>
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
"""
    files["src/views/CalcTemplateView.vue"] = """<template>
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
"""
    files["src/views/DataEntryView.vue"] = """<template>
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
"""
    files["src/views/ReportView.vue"] = """<template>
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
"""
    files["src/components/CrudPage.vue"] = """<template>
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
import { ElMessage, ElMessageBox } from "element-plus";
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
    ElMessage.success("更新成功");
  } else {
    await request.post(`${props.endpoint}/`, form);
    ElMessage.success("新增成功");
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
  ElMessage.success("删除成功");
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
"""
    files[".env.development"] = "VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1\n"
    return files


def write_files():
    """Write all generated frontend files."""
    root = Path(__file__).resolve().parent.parent
    files = build_files()
    for rel_path, content in files.items():
        full_path = root / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
    print(f"Wrote {len(files)} files.")


if __name__ == "__main__":
    write_files()

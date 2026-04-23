import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
import LoginView from "../views/LoginView.vue";
import MainLayout from "../layouts/MainLayout.vue";
import AxureView from "../views/AxureView.vue";
import FuelTypeView from "../views/FuelTypeView.vue";
import MaterialView from "../views/MaterialView.vue";
import CalcTemplateView from "../views/CalcTemplateView.vue";
import DataEntryView from "../views/DataEntryView.vue";
import ReportView from "../views/ReportView.vue";

const axureBaseUrl = import.meta.env.VITE_AXURE_BASE_URL || "/axure";
const axureUrl = (fileName) => `${axureBaseUrl}/${encodeURIComponent(fileName)}`;

const routes = [
  { path: "/login", component: LoginView, meta: { public: true } },
  { path: "/", redirect: "/dashboard" },
  { path: "/dashboard", component: AxureView, props: { src: axureUrl("碳画像总览.html") } },
  { path: "/calc/overview", component: AxureView, props: { src: axureUrl("能碳总览.html") } },
  { path: "/analysis/energy", component: AxureView, props: { src: axureUrl("能耗分析.html") } },
  { path: "/analysis/power", component: AxureView, props: { src: axureUrl("用电分析.html") } },
  {
    path: "/app",
    component: MainLayout,
    children: [
      { path: "", redirect: "/app/master/fuels" },
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
  if (to.meta.public) return true;
  const store = useAuthStore();
  if (!store.accessToken) return "/login";
  return true;
});

export default router;

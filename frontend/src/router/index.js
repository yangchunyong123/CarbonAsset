import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
import LoginView from "../views/LoginView.vue";
import MainLayout from "../layouts/MainLayout.vue";
import DashboardView from "../views/DashboardView.vue";
import FuelTypeView from "../views/FuelTypeView.vue";
import MaterialView from "../views/MaterialView.vue";
import CalcTemplateView from "../views/CalcTemplateView.vue";
import DataEntryView from "../views/DataEntryView.vue";
import ReportView from "../views/ReportView.vue";
import CalcOverviewView from "../views/CalcOverviewView.vue";
import PowerAnalysisView from "../views/PowerAnalysisView.vue";

const routes = [
  { path: "/login", component: LoginView, meta: { public: true } },
  {
    path: "/",
    component: MainLayout,
    children: [
      { path: "", redirect: "/dashboard" },
      { path: "dashboard", component: DashboardView },
      { path: "calc/overview", component: CalcOverviewView },
      { path: "analysis/power", component: PowerAnalysisView },
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

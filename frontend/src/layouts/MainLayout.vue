<template>
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

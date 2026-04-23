<template>
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

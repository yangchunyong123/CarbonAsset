<template>
  <div class="login-container">
    <!-- 左侧品牌展示区 -->
    <div class="left-section">
      <div class="left-content">
        <h1 class="company-title">英利发展</h1>
        <p class="company-desc">英利能源是中国最早投身光伏行业的企业之一，是集技术研发、智能制造、电站业务为一体的光伏智慧能源解决方案提供商。</p>
        <p class="company-desc">2023年光伏组件中标量及出货量位居行业前十，总部位于河北保定，产业布局保定、天津、衡水等多个基地。</p>
        <p class="company-desc">以卓越科技探索绿色光能大规模开发利用，为实现“双碳”目标贡献光伏智慧与力量。</p>
      </div>
    </div>

    <!-- 右侧登录表单区 -->
    <div class="right-section">
      <div class="login-box">
        <h2 class="welcome-title">欢迎回来</h2>
        
        <el-divider class="login-divider">
          <span class="divider-text">账号密码登录</span>
        </el-divider>

        <el-form :model="form" @submit.prevent class="login-form">
          <el-form-item>
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              :prefix-icon="User"
              class="custom-input"
            />
          </el-form-item>

          <el-form-item>
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              :prefix-icon="Lock"
              show-password
              class="custom-input"
              @keyup.enter="onLogin"
            />
          </el-form-item>

          <el-button
            type="primary"
            :loading="loading"
            class="login-button"
            @click="onLogin"
          >
            登 录
          </el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { ElNotification } from "element-plus";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { User, Lock } from "@element-plus/icons-vue";

const router = useRouter();
const auth = useAuthStore();
const loading = ref(false);
const form = reactive({ username: "admin", password: "123456" });

/**
 * Submit credentials and redirect to dashboard on success.
 */
async function onLogin() {
  if (!form.username || !form.password) {
    ElNotification({
      title: "提示",
      message: "请输入用户名和密码",
      type: "warning",
      duration: 3000,
    });
    return;
  }
  
  loading.value = true;
  try {
    await auth.login(form);
    ElNotification({
      title: "成功",
      message: "登录成功",
      type: "success",
      duration: 2000,
    });
    router.push("/dashboard");
  } catch (error) {
    ElNotification({
      title: "错误",
      message: "登录失败，请检查用户名或密码是否正确",
      type: "error",
      duration: 3000,
    });
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  overflow: hidden;
  background-color: #ffffff;
}

/* 左侧蓝色区域 */
.left-section {
  flex: 6.5;
  background-color: #005eb8;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  padding: 0 10%;
}

.left-content {
  max-width: 680px;
  margin-top: -50px;
}

.company-title {
  font-size: 42px;
  font-weight: 700;
  margin-bottom: 40px;
  letter-spacing: 2px;
}

.company-desc {
  font-size: 15px;
  line-height: 2.2;
  margin-bottom: 16px;
  opacity: 0.95;
  letter-spacing: 1px;
}

/* 右侧白色登录区域 */
.right-section {
  flex: 3.5;
  background-color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  min-width: 400px;
}

.login-box {
  width: 100%;
  max-width: 360px;
}

.welcome-title {
  font-size: 32px;
  font-weight: 700;
  color: #2c3e50;
  text-align: center;
  margin-bottom: 30px;
  letter-spacing: 2px;
}

.login-divider {
  margin-bottom: 40px;
}

.divider-text {
  color: #909399;
  font-size: 14px;
}

.login-form {
  margin-top: 10px;
}

/* 自定义输入框样式 */
.custom-input {
  height: 48px;
  margin-bottom: 6px;
}

:deep(.custom-input .el-input__wrapper) {
  border-radius: 4px;
  box-shadow: 0 0 0 1px #dcdfe6 inset;
}

:deep(.custom-input .el-input__wrapper:hover),
:deep(.custom-input .el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #005eb8 inset;
}

:deep(.custom-input .el-input__inner) {
  font-size: 15px;
}

:deep(.custom-input .el-input__prefix-inner) {
  font-size: 18px;
  color: #909399;
}

/* 登录按钮样式 */
.login-button {
  width: 100%;
  height: 48px;
  margin-top: 20px;
  border-radius: 24px;
  background-color: #005eb8;
  border-color: #005eb8;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 8px;
  text-indent: 8px; /* 补偿letter-spacing带来的居中偏移 */
}

.login-button:hover,
.login-button:focus {
  background-color: #004d99;
  border-color: #004d99;
}
</style>

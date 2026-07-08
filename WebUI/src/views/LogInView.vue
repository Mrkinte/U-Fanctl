<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useDialog, useMessage } from "naive-ui";
import { login } from "../apis/auth.ts";
import { useRouter } from "vue-router";

const router = useRouter();

const dialog = useDialog();
const message = useMessage();

const password = ref("");
const isLoggingIn = ref(false);
const rememberPassword = ref(false);

const handleLogIn = async () => {
  if (rememberPassword.value) {
    localStorage.setItem("password", password.value);
  } else {
    localStorage.removeItem("password");
  }
  if (password.value.length === 0) {
    message.info("密码不能为空");
    return;
  }
  const res = await login(password.value);
  if (res.result === "success") {
    router.push("/control-view");
  }
};

const handleForgetPassword = () => {
  dialog.info({
    title: "忘记密码",
    content:
      "如忘记密码，请查看配置文件。文件所在位置：软件安装目录/config.toml",
    positiveText: "确定",
  });
};

onMounted(() => {
  const storedPassword = localStorage.getItem("password");
  if (storedPassword) {
    password.value = storedPassword;
    rememberPassword.value = true;
  }
});
</script>

<template>
  <n-card class="login-card" hoverable>
    <n-flex vertical :size="24">
      <n-h1 class="title">U-NAS风扇控制软件</n-h1>
      <n-input
        v-model:value="password"
        class="password-input"
        type="password"
        size="large"
        show-password-toggle
        placeholder="请输入您的密码"
        @keydown.enter="handleLogIn"
      />
      <n-button
        class="login-button"
        size="large"
        :loading="isLoggingIn"
        @click="handleLogIn"
      >
        登录
      </n-button>
      <n-flex class="other-space" justify="space-between">
        <n-checkbox v-model:checked="rememberPassword">记住密码</n-checkbox>
        <n-button text @click="handleForgetPassword"> 忘记密码</n-button>
      </n-flex>
    </n-flex>
  </n-card>
</template>

<style scoped>
.login-card {
  max-width: 400px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.title {
  text-align: center;
  font-weight: bold;
}

.password-input {
  width: 100%;
}

.login-button {
  width: 100%;
}

@media (max-width: 540px) {
  .login-card {
    max-width: 94%;
  }
}
</style>

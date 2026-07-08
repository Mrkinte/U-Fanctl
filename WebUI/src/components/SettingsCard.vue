<script setup lang="ts">
import { title, ws } from "../models/global.ts";
import { useRouter } from "vue-router";
import { logout } from "../apis/auth.ts";
import { ref } from "vue";
import { resetPasswordConfig, setSystemConfig } from "../apis/config.ts";
import { useMessage } from "naive-ui";

const router = useRouter();
const message = useMessage();

const inputTitle = ref(title.value);
const oldPassword = ref("");
const newPassword = ref("");

const handleLogout = async () => {
  if (ws.value !== undefined) ws.value.close();
  try {
    await logout();
  } finally {
    router.push("/");
  }
};

const handleSetTitle = async () => {
  title.value = inputTitle.value;
  const res = await setSystemConfig(title.value);
  if (res.result === "success") {
    message.success("设置成功");
  } else {
    message.error("设置失败：" + res.detail);
  }
};

const handleResetPassword = async () => {
  if (oldPassword.value.length === 0 || newPassword.value.length === 0) {
    message.error("密码不能为空");
    return;
  }
  const res = await resetPasswordConfig(oldPassword.value, newPassword.value);
  if (res.result === "success") {
    message.success("重置成功");
    try {
      await logout();
    } finally {
      router.push("/");
    }
  } else {
    message.error("重置失败：" + res.detail);
  }
};
</script>

<template>
  <div class="settings-card">
    <n-card hoverable>
      <n-flex vertical :size="24">
        <n-h1>设置</n-h1>
        <n-flex vertical>
          <n-text>自定义标题</n-text>
          <n-input v-model:value="inputTitle" placeholder="U-NAS" />
          <n-flex justify="end">
            <n-button @click="handleSetTitle">应用修改</n-button>
          </n-flex>
        </n-flex>
        <n-flex vertical>
          <n-text>重置密码</n-text>
          <n-input
            v-model:value="oldPassword"
            type="password"
            show-password-toggle
            placeholder="请输入旧密码"
          />
          <n-tooltip>
            <template #trigger>
              <n-input
                v-model:value="newPassword"
                type="password"
                show-password-toggle
                placeholder="请输入新密码"
              />
            </template>
            仅支持大写字母、小写字母和数字，密码长度1-16。
          </n-tooltip>
          <n-flex justify="end">
            <n-button @click="handleResetPassword">确认重置</n-button>
          </n-flex>
        </n-flex>
        <n-button type="primary" @click="handleLogout">退出登录</n-button>
      </n-flex>
    </n-card>
  </div>
</template>

<style scoped>
.n-h1 {
  text-align: center;
}

.settings-card {
  width: 400px;
  display: flex;
}
</style>

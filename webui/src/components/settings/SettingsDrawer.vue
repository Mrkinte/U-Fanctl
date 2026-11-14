<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useMessage } from "naive-ui";
import { useRouter } from "vue-router";
import {
  getTemperatureApiV1TemperatureGet,
  logoutApiV1AuthLogoutPost,
  updatePasswordApiV1AuthPasswordPut,
  updateSystemApiV1SystemPut,
  updateTemperatureApiV1TemperaturePut,
  type TemperatureSettings,
} from "../../api/generated";
import { temperatureSettings, title } from "../../composables/useAppState";
import { useDeviceStatus } from "../../composables/useDeviceStatus";

const show = defineModel<boolean>("show");

const router = useRouter();
const message = useMessage();
const { disconnect: disconnectSocket } = useDeviceStatus();

const inputTitle = ref(title.value);
const temperatureSource = ref<TemperatureSettings["source"]>("cpu");
const temperatureInterval = ref<number | null>(1);
const oldPassword = ref("");
const newPassword = ref("");

const sourceOptions: { label: string; value: TemperatureSettings["source"] }[] = [
  { label: "CPU", value: "cpu" },
  { label: "硬盘", value: "hdd" },
];

const mobileQuery = window.matchMedia("(max-width: 540px)");
const isMobile = ref(mobileQuery.matches);
const drawerWidth = computed(() => (isMobile.value ? "100%" : "360px"));

const syncDrawerWidth = () => {
  isMobile.value = mobileQuery.matches;
};

const loadTemperatureSettings = async () => {
  const { data } = await getTemperatureApiV1TemperatureGet();
  if (data) {
    temperatureSource.value = data.source;
    temperatureInterval.value = data.interval;
  }
};

const handleApplyTitle = async () => {
  const { error } = await updateSystemApiV1SystemPut({
    body: { title: inputTitle.value },
  });
  if (error === undefined) {
    title.value = inputTitle.value;
    message.success("设置成功");
  }
};

const handleApplyTemperature = async () => {
  const source = temperatureSource.value;
  const interval = temperatureInterval.value ?? 1;
  const { error } = await updateTemperatureApiV1TemperaturePut({
    body: { source, interval },
  });
  if (error === undefined) {
    temperatureSettings.value = { source, interval };
    message.success("设置成功");
  }
};

const handleResetPassword = async () => {
  if (oldPassword.value.length === 0 || newPassword.value.length === 0) {
    message.warning("密码不能为空");
    return;
  }
  const { error } = await updatePasswordApiV1AuthPasswordPut({
    body: {
      old_password: oldPassword.value,
      new_password: newPassword.value,
    },
  });
  if (error === undefined) {
    message.success("重置成功");
    await logoutApiV1AuthLogoutPost();
    show.value = false;
    router.push("/");
  }
};

const handleLogout = async () => {
  disconnectSocket();
  await logoutApiV1AuthLogoutPost();
  show.value = false;
  router.push("/");
};

watch(show, async (visible) => {
  if (!visible) {
    return;
  }
  inputTitle.value = title.value;
  oldPassword.value = "";
  newPassword.value = "";
  await loadTemperatureSettings();
});

onMounted(() => {
  syncDrawerWidth();
  window.addEventListener("resize", syncDrawerWidth);
  mobileQuery.addEventListener("change", syncDrawerWidth);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", syncDrawerWidth);
  mobileQuery.removeEventListener("change", syncDrawerWidth);
});
</script>

<template>
  <n-drawer v-model:show="show" :width="drawerWidth" placement="right">
    <n-drawer-content title="设置" closable>
      <n-flex vertical :size="24">
        <section class="settings-group">
          <n-divider title-placement="left">网站设置</n-divider>
          <n-form label-placement="top" :show-feedback="false">
            <n-form-item label="网站标题">
              <n-input v-model:value="inputTitle" placeholder="U-NAS" />
            </n-form-item>
          </n-form>
          <n-flex justify="end">
            <n-button @click="handleApplyTitle">应用修改</n-button>
          </n-flex>
        </section>
        <section class="settings-group">
          <n-divider title-placement="left">硬件</n-divider>
          <n-form label-placement="top" :show-feedback="false">
            <n-form-item label="温度采集源">
              <n-select v-model:value="temperatureSource" :options="sourceOptions" />
            </n-form-item>
            <n-form-item label="采集间隔">
              <n-input-number
                v-model:value="temperatureInterval"
                :min="1"
                :max="60"
                class="interval-input"
              >
                <template #suffix>秒</template>
              </n-input-number>
            </n-form-item>
          </n-form>
          <n-flex justify="end">
            <n-button @click="handleApplyTemperature">应用修改</n-button>
          </n-flex>
        </section>
        <section class="settings-group">
          <n-divider title-placement="left">安全</n-divider>
          <n-form label-placement="top" :show-feedback="false">
            <n-form-item label="旧密码">
              <n-input
                v-model:value="oldPassword"
                type="password"
                show-password-toggle
                placeholder="请输入旧密码"
              />
            </n-form-item>
            <n-form-item label="新密码">
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
            </n-form-item>
          </n-form>
          <n-flex justify="end">
            <n-button @click="handleResetPassword">确认重置</n-button>
          </n-flex>
        </section>
        <n-button type="primary" @click="handleLogout">退出登录</n-button>
      </n-flex>
    </n-drawer-content>
  </n-drawer>
</template>

<style scoped>
.settings-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.settings-group :deep(.n-divider) {
  margin: 0;
}

.settings-group :deep(.n-form-item) {
  margin-bottom: 16px;
}

.settings-group :deep(.n-form-item:last-child) {
  margin-bottom: 0;
}

.interval-input {
  width: 100%;
}
</style>

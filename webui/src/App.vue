<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { type GlobalThemeOverrides } from "naive-ui";
import { Settings24Regular, WeatherMoon24Filled, WeatherSunny24Regular } from "@vicons/fluent";
import { useRoute } from "vue-router";
import { getSystemApiV1SystemGet } from "./api/generated";
import SettingsDrawer from "./components/settings/SettingsDrawer.vue";
import { title, version } from "./composables/useAppState";
import { currentTheme, toggleTheme } from "./composables/useTheme";

const route = useRoute();
const showSettings = ref(false);

const themeOverrides: GlobalThemeOverrides = {
  common: {
    borderRadius: "6px",
  },
  Layout: {
    footerColor: "transparent",
  },
};

const badgeUrl = computed(
  () => `https://img.shields.io/badge/Version-${version.value}-brightgreen?style=flat-square`,
);

const handleGithub = () => {
  window.open("https://github.com/mrkinte/U-Fanctl", "_blank");
};

watch(
  title,
  (value) => {
    document.title = value;
  },
  { immediate: true },
);

onMounted(async () => {
  const { data } = await getSystemApiV1SystemGet();
  if (data) {
    title.value = data.title;
    version.value = data.version;
  }
});
</script>

<template>
  <n-config-provider :theme="currentTheme" :theme-overrides="themeOverrides">
    <n-dialog-provider>
      <n-message-provider>
        <div id="root-container">
          <n-layout>
            <n-layout-header class="header">
              <span class="title-span">{{ title }}</span>
              <n-flex align="center" size="large">
                <n-button
                  v-if="route.name === 'ControlView'"
                  text
                  class="settings-button"
                  @click="showSettings = true"
                >
                  <n-icon>
                    <Settings24Regular />
                  </n-icon>
                </n-button>
                <n-button text class="theme-button" @click="toggleTheme">
                  <n-icon>
                    <WeatherMoon24Filled v-if="currentTheme.name === 'light'" />
                    <WeatherSunny24Regular v-else />
                  </n-icon>
                </n-button>
                <img :src="badgeUrl" alt="version" />
              </n-flex>
            </n-layout-header>
            <n-layout-content class="content" :native-scrollbar="false">
              <router-view />
            </n-layout-content>
            <n-layout-footer class="footer">
              <div class="github-link">
                <n-button text @click="handleGithub">
                  <template #icon>
                    <svg
                      aria-hidden="true"
                      focusable="false"
                      viewBox="0 0 24 24"
                      width="24"
                      height="24"
                      fill="currentColor"
                      overflow="visible"
                      class="github-icon"
                    >
                      <path
                        d="M12 1C5.923 1 1 5.923 1 12c0 4.867 3.149 8.979 7.521 10.436.55.096.756-.233.756-.522 0-.262-.013-1.128-.013-2.049-2.764.509-3.479-.674-3.699-1.292-.124-.317-.66-1.293-1.127-1.554-.385-.207-.936-.715-.014-.729.866-.014 1.485.797 1.691 1.128.99 1.663 2.571 1.196 3.204.907.096-.715.385-1.196.701-1.471-2.448-.275-5.005-1.224-5.005-5.432 0-1.196.426-2.186 1.128-2.956-.111-.275-.496-1.402.11-2.915 0 0 .921-.288 3.024 1.128a10.193 10.193 0 0 1 2.75-.371c.936 0 1.871.123 2.75.371 2.104-1.43 3.025-1.128 3.025-1.128.605 1.513.221 2.64.111 2.915.701.77 1.127 1.747 1.127 2.956 0 4.222-2.571 5.157-5.019 5.432.399.344.743 1.004.743 2.035 0 1.471-.014 2.654-.014 3.025 0 .289.206.632.756.522C19.851 20.979 23 16.854 23 12c0-6.077-4.922-11-11-11Z"
                      />
                    </svg>
                  </template>
                  Github
                </n-button>
              </div>
            </n-layout-footer>
          </n-layout>
        </div>
        <SettingsDrawer v-model:show="showSettings" />
      </n-message-provider>
    </n-dialog-provider>
    <n-global-style />
  </n-config-provider>
</template>

<style scoped>
#root-container {
  width: 100vw;
  height: 100vh;
  display: flex;
}

.header {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;

  .title-span {
    font-size: 2rem;
  }
}

.settings-button,
.theme-button {
  font-size: 24px;
}

.content {
  height: calc(100% - 96px);
}

.footer {
  height: 48px;
  display: flex;
  justify-content: center;
}

.github-icon {
  vertical-align: text-bottom;
}
</style>

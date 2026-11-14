<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import { useDialog } from "naive-ui";
import { useRouter } from "vue-router";
import { getTemperatureApiV1TemperatureGet } from "../api/generated";
import ControlModeCard from "../components/control/ControlModeCard.vue";
import CurveEditorCard from "../components/control/CurveEditorCard.vue";
import TemperatureChartCard from "../components/dashboard/TemperatureChartCard.vue";
import { temperatureSettings } from "../composables/useAppState";
import { useDeviceStatus } from "../composables/useDeviceStatus";

const router = useRouter();
const dialog = useDialog();

const chartRef = ref<InstanceType<typeof TemperatureChartCard> | null>(null);

const { connect, disconnect } = useDeviceStatus({
  onTemperature: (temperature) => chartRef.value?.pushTemperature(temperature),
});

const loadTemperatureSettings = async () => {
  const { data } = await getTemperatureApiV1TemperatureGet();
  if (data) {
    temperatureSettings.value = data;
  }
};

onMounted(async () => {
  const temperatureRequest = loadTemperatureSettings();
  const connected = await connect();
  if (!connected) {
    dialog.warning({
      title: "登录超时",
      content: "当前会话已失效，请重新登录。",
      positiveText: "确定",
    });
    router.push("/");
    return;
  }
  await temperatureRequest;
});

onBeforeUnmount(() => {
  disconnect();
});
</script>

<template>
  <div id="control-view">
    <ControlModeCard />
    <CurveEditorCard />
    <TemperatureChartCard ref="chartRef" :source="temperatureSettings.source" />
  </div>
</template>

<style scoped>
#control-view {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(640px, 1fr));
  gap: 24px;
  padding: 24px;
}

@media (max-width: 540px) {
  #control-view {
    padding: 8px;
  }
}
</style>

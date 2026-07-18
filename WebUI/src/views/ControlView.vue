<script setup lang="ts">
import ControlMode from "../components/ControlMode.vue";
import ControlCurve from "../components/ControlCurve.vue";
import SettingsCard from "../components/SettingsCard.vue";
import { onMounted, ref } from "vue";
import { deviceStatus, ws } from "../models/global.ts";
import { getWebSocketBaseUrl } from "../utils/custom.ts";
import type { DeviceStatus } from "../models/config-model.ts";
import type TemperatureChart from "../components/TemperatureChart.vue";

const heartbeatTimer = ref(0);
const chartRef = ref<InstanceType<typeof TemperatureChart> | null>(null);

const handlePushTemperature = (temp: number) => {
  chartRef.value?.pushTemperature(temp);
};

onMounted(() => {
  if (ws.value !== undefined) return;

  ws.value = new WebSocket(`${getWebSocketBaseUrl()}/api/v1/ws/info`);

  ws.value.onclose = () => {
    clearInterval(heartbeatTimer.value);
    ws.value = undefined;
  };

  ws.value.onmessage = (event: MessageEvent) => {
    const rawData: string = event.data;
    const parsedData = JSON.parse(rawData);
    deviceStatus.value = parsedData as DeviceStatus;
    handlePushTemperature(deviceStatus.value.temperature);
  };

  heartbeatTimer.value = setInterval(() => {
    if (ws.value === undefined) return;
    ws.value.send("heartbeat");
  }, 5000);
});
</script>

<template>
  <div id="control-view">
    <ControlMode />
    <ControlCurve />
    <TemperatureChart ref="chartRef" />
    <SettingsCard />
  </div>
</template>

<style scoped>
#control-view {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  padding: 24px;
  align-items: stretch;
}

@media (max-width: 540px) {
  #control-view {
    padding: 8px;
  }
}
</style>

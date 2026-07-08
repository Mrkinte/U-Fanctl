import { ref } from "vue";
import type { DeviceStatus } from "./config-model.ts";

export const title = ref("U-NAS");
export const version = ref("0.0.0");
export const deviceStatus = ref<DeviceStatus>({
  temperature: 0,
  fan_speed: 0,
});
export const ws = ref<WebSocket | undefined>(undefined);

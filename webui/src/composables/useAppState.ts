import { ref } from "vue";
import type { TemperatureSettings } from "../api/generated";

export interface StatusMessage {
  temperature: number;
  fan_speed: number;
  source: TemperatureSettings["source"];
}

export const title = ref("U-NAS");
export const version = ref("0.0.0");
export const temperatureSettings = ref<TemperatureSettings>({
  source: "cpu",
  interval: 1,
});
export const deviceStatus = ref<StatusMessage>({
  temperature: 0,
  fan_speed: 0,
  source: "cpu",
});

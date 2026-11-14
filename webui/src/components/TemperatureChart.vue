<script setup lang="ts">
import { computed, ref } from "vue";
import type { EChartsOption } from "echarts";
import VChart from "vue-echarts";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { LineChart } from "echarts/charts";
import { GridComponent, TooltipComponent } from "echarts/components";
import wonderland from "../assets/wonderland.json";
import * as echarts from "echarts";
import { DismissCircle32Filled } from "@vicons/fluent";
echarts.registerTheme("wonderland", wonderland);

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent]);

const MAX_DURATION = 60 * 1000;
const nowRef = ref(Date.now());
const errorVisibility = ref(false);

const tempData = ref<[number, number][]>(
  Array.from({ length: 61 }, (_, i) => {
    const t = Date.now() - (60 - i) * 1000;
    return [t, null as unknown as number];
  }),
);

const option = computed<EChartsOption>(() => ({
  tooltip: {
    trigger: "axis",
    formatter: (params: unknown) => {
      const p = params as { value: [number, number] }[];
      if (!p || p.length === 0) return "";
      const val = p[0].value[1];
      return val != null ? `${val.toFixed(1)}°C` : "无数据";
    },
  },
  xAxis: {
    type: "time",
    max: nowRef.value,
    min: nowRef.value - MAX_DURATION,
    splitNumber: 4,
    axisLabel: {
      formatter: (value: number) => {
        const ago = Math.round((nowRef.value - value) / 1000);
        if (ago === 0) return "0s";
        if (ago === 60) return "60s";
        return `${ago}s`;
      },
    },
  },
  yAxis: {
    type: "value",
    name: "°C",
    min: 0,
    max: 100,
  },
  series: [
    {
      type: "line",
      data: tempData.value,
      showSymbol: false,
      animation: false,
      smooth: true,
      areaStyle: { opacity: 0.2 },
    },
  ],
}));

const pushTemperature = (temp: number) => {
  if (temp <= -1) {
    errorVisibility.value = true;
    return;
  } else {
    errorVisibility.value = false;
  }

  const now = Date.now();
  nowRef.value = now;
  tempData.value = [...tempData.value.slice(1), [now, temp]];
};
defineExpose({ pushTemperature });
</script>

<template>
  <div class="temperature-chart">
    <n-card hoverable>
      <n-h1 class="chart-title">CPU温度</n-h1>
      <n-tooltip>
        <template #trigger>
          <div
            style="
              position: absolute;
              top: 50%;
              left: 50%;
              transform: translate(-50%, -50%);
              z-index: 1;
            "
          >
            <n-tag v-if="errorVisibility" round :bordered="false" type="error">
              <template #icon>
                <n-icon>
                  <DismissCircle32Filled />
                </n-icon>
              </template>
              无法获取温度数据
            </n-tag>
          </div>
        </template>
        若您在虚拟机上运行该软件，可能无法准确获取CPU温度信息。
      </n-tooltip>
      <v-chart class="chart" :option="option" theme="wonderland" autoresize />
    </n-card>
  </div>
</template>

<style scoped>
.temperature-chart {
  min-width: 640px;
  display: flex;
}

.chart-title {
  text-align: center;
}

.chart {
  width: 100%;
  height: 320px;
}
</style>

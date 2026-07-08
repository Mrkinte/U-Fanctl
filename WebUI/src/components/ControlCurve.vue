<script setup lang="ts">
import { computed, nextTick, onMounted, onUnmounted, ref } from "vue";
import type { EChartsOption } from "echarts";
import VChart from "vue-echarts";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { LineChart } from "echarts/charts";
import {
  GridComponent,
  GraphicComponent,
  TooltipComponent,
} from "echarts/components";
import wonderland from "../assets/wonderland.json";
import * as echarts from "echarts";
import { getCurveConfig, setCurveConfig } from "../apis/config.ts";
import type { CurveConfig } from "../models/config-model.ts";
import { useMessage } from "naive-ui";
echarts.registerTheme("wonderland", wonderland);

use([
  CanvasRenderer,
  LineChart,
  GridComponent,
  GraphicComponent,
  TooltipComponent,
]);
const message = useMessage();

const TEMPERATURE_LABELS = [
  "30°C",
  "40°C",
  "50°C",
  "60°C",
  "70°C",
  "80°C",
  "90°C",
  "100°C",
];

const curveData = ref<number[]>([0, 0, 0, 0, 0, 0, 0, 0]);

const chartRef = ref<InstanceType<typeof VChart>>();
function getChart() {
  return chartRef.value?.chart;
}

const option = computed<EChartsOption>(() => ({
  tooltip: {
    trigger: "axis",
    formatter: (params: unknown) => {
      const p = params as { name: string; value: number }[];
      if (!p || p.length === 0) return "";
      const item = p[0];
      return `${item.value}%`;
    },
  },
  xAxis: {
    type: "category",
    data: TEMPERATURE_LABELS,
    name: "温度",
  },
  yAxis: {
    type: "value",
    min: 0,
    max: 100,
    name: "转速",
    axisLabel: {
      formatter: (value: number) =>
        value === 0 || value === 100 ? value + "%" : "",
    },
  },
  series: [
    {
      type: "line",
      data: curveData.value,
      symbol: "circle",
      symbolSize: 14,
      emphasis: {
        symbolSize: 20,
        scale: true,
      },
    },
  ],
}));

const updateGraphic = () => {
  const chart = getChart();
  if (!chart) return;

  const graphicItems = curveData.value.map((val, idx) => {
    const pixel = chart.convertToPixel("grid", [idx, val]) as number[];
    return {
      type: "circle" as const,
      shape: { r: 8 },
      x: pixel[0],
      y: pixel[1],
      invisible: true,
      draggable: "vertical" as const,
      z: 100,
      ondrag: function (this: { x: number; y: number }) {
        const c = getChart();
        if (!c) return;
        const pixelFrom = c.convertFromPixel("grid", [
          this.x,
          this.y,
        ]) as number[];
        const clampedY = Math.max(0, Math.min(100, Math.round(pixelFrom[1])));
        const newData = [...curveData.value];
        newData[idx] = clampedY;
        // 左侧点值 > clampedY → 下拉
        for (let i = 0; i < idx; i++) {
          if (newData[i] > clampedY) newData[i] = clampedY;
        }
        // 右侧点值 < clampedY → 上拉
        for (let i = idx + 1; i < newData.length; i++) {
          if (newData[i] < clampedY) newData[i] = clampedY;
        }
        curveData.value = newData;
        requestAnimationFrame(updateGraphic);
      },
    };
  });

  chart.setOption({ graphic: graphicItems });
};

const handleApply = async () => {
  const conf = ref<CurveConfig>({
    t30: curveData.value[0],
    t40: curveData.value[1],
    t50: curveData.value[2],
    t60: curveData.value[3],
    t70: curveData.value[4],
    t80: curveData.value[5],
    t90: curveData.value[6],
    t100: curveData.value[7],
  });
  const res = await setCurveConfig(conf.value);
  if (res.result === "success") {
    message.success("设置成功");
  }
};

const handleRestoreDefaultCurve = async () => {
  await handleGetCurveConfig(true);
  await handleApply();
};

const handleGetCurveConfig = async (defaults: boolean = false) => {
  const res = await getCurveConfig(defaults);
  if (res.result === "success") {
    curveData.value[0] = res.data.t30;
    curveData.value[1] = res.data.t40;
    curveData.value[2] = res.data.t50;
    curveData.value[3] = res.data.t60;
    curveData.value[4] = res.data.t70;
    curveData.value[5] = res.data.t80;
    curveData.value[6] = res.data.t90;
    curveData.value[7] = res.data.t100;
  }
};

const onResize = () => {
  updateGraphic();
};

onMounted(async () => {
  await handleGetCurveConfig();
  window.addEventListener("resize", onResize);
  await nextTick();
  updateGraphic();
});

onUnmounted(() => {
  window.removeEventListener("resize", onResize);
});
</script>

<template>
  <div class="control-curve">
    <n-card hoverable>
      <n-h1 class="curve-title">温度调节曲线</n-h1>
      <n-flex vertical :size="24">
        <v-chart
          ref="chartRef"
          class="chart"
          :option="option"
          theme="wonderland"
          autoresize
          style="touch-action: none"
        />
        <n-flex justify="end">
          <n-button @click="handleRestoreDefaultCurve">恢复默认</n-button>
          <n-button @click="handleApply">应用修改</n-button>
        </n-flex>
      </n-flex>
    </n-card>
  </div>
</template>

<style scoped>
.control-curve {
  width: 800px;
  display: flex;
}

.curve-title {
  text-align: center;
}

.chart {
  width: 100%;
  height: 320px;
  cursor: pointer;
}
</style>

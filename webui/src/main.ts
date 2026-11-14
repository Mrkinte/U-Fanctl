import { createApp } from "vue";
import "./styles/global.css";
import "./styles/echarts-theme";
import "./api/client";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);
app.use(router).mount("#app");

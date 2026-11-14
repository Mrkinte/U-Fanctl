import { createRouter, createWebHistory } from "vue-router";
import LogInView from "../views/LogInView.vue";
import ControlView from "../views/ControlView.vue";

const routes = [
  {
    path: "/",
    name: "Login",
    component: LogInView,
  },
  {
    path: "/control-view",
    name: "ControlView",
    component: ControlView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

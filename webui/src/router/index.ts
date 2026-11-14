import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import ControlView from "../views/ControlView.vue";

const routes = [
  {
    path: "/",
    name: "Login",
    component: LoginView,
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

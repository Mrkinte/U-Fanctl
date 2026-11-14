import { computed, ref } from "vue";
import { darkTheme, lightTheme } from "naive-ui";

const STORAGE_KEY = "theme";

const isLight = ref(localStorage.getItem(STORAGE_KEY) === "light");

export const currentTheme = computed(() => (isLight.value ? lightTheme : darkTheme));

export const toggleTheme = () => {
  isLight.value = !isLight.value;
  localStorage.setItem(STORAGE_KEY, isLight.value ? "light" : "dark");
};

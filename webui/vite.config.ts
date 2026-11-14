import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import Components from "unplugin-vue-components/vite";
import { NaiveUiResolver } from "unplugin-vue-components/resolvers";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [NaiveUiResolver()],
    }),
  ],
  server:
    process.env.NODE_ENV === "development"
      ? {
          host: "0.0.0.0",
          proxy: {
            "/api": {
              target: "http://127.0.0.1:3233",
              changeOrigin: true,
              secure: false, // 禁用 SSL验证（测试环境使用）
            },
          },
        }
      : undefined,
  build: {
    outDir: "../src/wwwroot",
  },
});

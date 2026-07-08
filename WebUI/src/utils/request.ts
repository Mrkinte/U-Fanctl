import axios from "axios";
import { getMessage } from "./message.ts";

const instance = axios.create({
  baseURL: "/api/v1",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

instance.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

instance.interceptors.response.use(
  (response) => {
    return response.data;
  },

  (error) => {
    const message = getMessage();
    // 常见 HTTP 错误统一处理
    if (error.response) {
      const status = error.response.status;
      const detail = error.response.data.detail;
      switch (status) {
        case 401:
          message.error(detail);
          break;
        case 403:
          message.error(detail);
          break;
        case 500:
          message.error(detail);
          break;
        default:
          message.error(`请求错误 ${status} ${detail}`);
      }
    } else if (error.message.includes("timeout")) {
      message.error("请求超时，请检查网络");
    } else {
      message.error("网络异常");
    }
    return Promise.reject(error);
  },
);

export default instance;

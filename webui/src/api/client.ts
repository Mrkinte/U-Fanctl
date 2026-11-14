import { createDiscreteApi } from "naive-ui";
import { client } from "./generated/client.gen";

const { message } = createDiscreteApi(["message"]);

client.setConfig({
  baseUrl: "",
  credentials: "include",
});

const SESSION_PATH = "/api/v1/auth/session";

const describeError = (status: number | undefined, error: unknown): string => {
  const detail = (error as { detail?: unknown } | undefined)?.detail;

  if (typeof detail === "string" && detail.length > 0) {
    return detail;
  }
  if (Array.isArray(detail)) {
    return "参数校验失败";
  }
  if (status === undefined) {
    return "网络异常，请检查连接";
  }

  switch (status) {
    case 401:
      return "会话已过期，请重新登录";
    case 403:
      return "没有权限执行该操作";
    case 404:
      return "请求的资源不存在";
    case 500:
      return "服务器内部错误";
    default:
      return `请求失败（${status}）`;
  }
};

client.interceptors.error.use((error, response, _request, options) => {
  const status = response?.status;
  if (status === 401 && options.url === SESSION_PATH) {
    return error;
  }

  message.error(describeError(status, error));
  return error;
});

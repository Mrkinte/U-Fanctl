/**
 * 动态获取IP
 */
export const getApiBaseUrl = () => {
  if (import.meta.env.DEV) {
    return "localhost:3233";
  }
  return window.location.host;
};

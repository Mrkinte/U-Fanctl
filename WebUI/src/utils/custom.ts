/**
 * 动态获取IP
 */
export const getApiBaseUrl = () => {
  if (import.meta.env.DEV) {
    return "localhost:3233";
  }
  return window.location.host;
};


export const getWebSocketBaseUrl = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = getApiBaseUrl();
  return `${protocol}//${host}`;
};
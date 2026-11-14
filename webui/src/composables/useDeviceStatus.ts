import { onBeforeUnmount } from "vue";
import { sessionApiV1AuthSessionGet } from "../api/generated";
import { deviceStatus, type StatusMessage } from "./useAppState";

interface DeviceStatusOptions {
  onTemperature?: (temperature: number) => void;
}

const HEARTBEAT_INTERVAL = 5000;

let socket: WebSocket | undefined;
let heartbeatTimer: number | undefined;
let connecting: Promise<boolean> | undefined;

const stopHeartbeat = () => {
  if (heartbeatTimer !== undefined) {
    window.clearInterval(heartbeatTimer);
    heartbeatTimer = undefined;
  }
};

const disconnect = () => {
  stopHeartbeat();
  if (socket === undefined) {
    return;
  }
  socket.onclose = null;
  socket.close();
  socket = undefined;
};

const buildSocketUrl = () => {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${protocol}//${window.location.host}/api/v1/ws/status`;
};

const openSocket = async (options: DeviceStatusOptions): Promise<boolean> => {
  if (socket !== undefined) {
    return true;
  }

  const { error } = await sessionApiV1AuthSessionGet();
  if (error !== undefined) {
    return false;
  }

  const ws = new WebSocket(buildSocketUrl());
  socket = ws;

  ws.onmessage = (event: MessageEvent<string>) => {
    const status = JSON.parse(event.data) as StatusMessage;
    deviceStatus.value = status;
    options.onTemperature?.(status.temperature);
  };

  ws.onclose = () => {
    if (socket === ws) {
      socket = undefined;
    }
    stopHeartbeat();
  };

  heartbeatTimer = window.setInterval(() => {
    if (socket?.readyState === WebSocket.OPEN) {
      socket.send("heartbeat");
    }
  }, HEARTBEAT_INTERVAL);

  return true;
};

export const useDeviceStatus = (options: DeviceStatusOptions = {}) => {
  const connect = (): Promise<boolean> => {
    if (socket !== undefined) {
      return Promise.resolve(true);
    }
    if (connecting === undefined) {
      connecting = openSocket(options).finally(() => {
        connecting = undefined;
      });
    }
    return connecting;
  };

  onBeforeUnmount(disconnect);

  return { connect, disconnect };
};

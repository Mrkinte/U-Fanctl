import type { MessageApi } from "naive-ui";

let messageInstance: MessageApi | null = null;

export function setMessageInstance(instance: MessageApi) {
  messageInstance = instance;
}

export function getMessage() {
  if (!messageInstance) {
    console.warn("Message instance not initialized, use fallback");
    throw new Error(
      "Message instance not initialized! Call setMessageInstance in App.vue",
    );
  }
  return messageInstance;
}

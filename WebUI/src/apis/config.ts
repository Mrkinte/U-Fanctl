import request from "../utils/request.ts";
import type { CustomResponse } from "../models/response-schemas.ts";
import type { ControlConfig, CurveConfig } from "../models/config-model.ts";

export async function getSystemConfig() {
  return (await request.get("/config/get/system")) as CustomResponse;
}

export async function getControlConfig() {
  return (await request.get("/config/get/control")) as CustomResponse;
}

export async function getCurveConfig(fromDefaults: boolean = false) {
  const url = fromDefaults
    ? "/config/get/curve?defaults=true"
    : "/config/get/curve";
  return (await request.get(url)) as CustomResponse;
}

export async function setSystemConfig(titleStr: string) {
  return (await request.post("/config/set/system", {
    title: titleStr,
  })) as CustomResponse;
}

export async function resetPasswordConfig(
  oldPassword: string,
  newPassword: string,
) {
  return (await request.post("/config/set/password", {
    old_password: oldPassword,
    new_password: newPassword,
  })) as CustomResponse;
}

export async function setControlConfig(conf: ControlConfig) {
  return (await request.post("/config/set/control", conf)) as CustomResponse;
}

export async function setCurveConfig(conf: CurveConfig) {
  return (await request.post("/config/set/curve", conf)) as CustomResponse;
}

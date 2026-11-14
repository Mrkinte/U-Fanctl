import request from "../utils/request.ts";
import type { CustomResponse } from "../models/response-schemas.ts";

export async function login(password: string) {
  return (await request.post("/auth/login", { password })) as CustomResponse;
}

export async function logout() {
  await request.get("/auth/logout");
}

export async function LoginDetection() {
  return (await request.get("/auth/login-detection")) as CustomResponse;
}

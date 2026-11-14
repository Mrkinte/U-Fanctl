export interface SystemConfig {
  title: string;
  version: string;
}

export interface ControlConfig {
  i2c_is_valid: boolean;
  manual: boolean;
  manual_speed: number;
}

export interface CurveConfig {
  t30: number;
  t40: number;
  t50: number;
  t60: number;
  t70: number;
  t80: number;
  t90: number;
  t100: number;
}

export interface DeviceStatus {
  temperature: number;
  fan_speed: number;
}

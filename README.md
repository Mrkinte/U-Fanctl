# U-Fanctl 万由U-NAS风扇控制软件
![技术栈](https://img.shields.io/badge/%E6%8A%80%E6%9C%AF%E6%A0%88-Python_+_Vue3_+_Vite-brightgreen?style=flat-square)
![开发工具](https://img.shields.io/badge/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7-WebStorm_+_PyCharm-blue?style=flat-square)
![许可证](https://img.shields.io/github/license/antonkomarev/github-profile-views-counter.svg?style=flat-square)

## 项目简介
这是一款为万由U-NAS（HS-201P）开发的、适配飞牛FnOS的风扇控制软件。众所周知，HS-201P自带的风扇满速运行时噪音较大，安装其他NAS系统后会默认满速运行。使用该软件后，可以手动设置温度曲线，实现自动调节风扇转速。

## 软件界面
![ControlView](https://github.com/Mrkinte/U-Fanctl/blob/main/Docs/ControlView.png?raw=true)

## 使用方法
- 下载 [u-fanctl.fpk](https://github.com/Mrkinte/U-Fanctl/releases/latest)

- 打开飞牛OS的 ```应用中心``` -> ```手动安装``` （位于左下角），根据提示信息进行安装即可。

## 注意事项
- 默认密码：admin

- 默认端口：3233

- 适用于HS-201P

- 通过i2c总线控制风扇，需要root权限。如果显示i2c未就绪，请检查系统是否正确加载了该模块。

- 仅适用基于Linux的NAS系统，目前也仅提供Fnos的安装包.fpk，其他NAS系统请自行打包。

## 项目结构

- ```src/```：后端 Python/FastAPI 服务，核心包为 `src/fanctl/`（`api`、`core`、`schemas`、`services`），入口为 `src/main.py`。

- ```webui/```：Vue3 + Vite + TypeScript 前端，构建输出到 `src/wwwroot`。

- ```fnos-package/```：飞牛 fpk 打包文件，详情请查阅 [飞牛官方文档](https://developer.fnnas.com/docs/guide)。

- ```build-script.sh```：自动化构建脚本，一键编译 fpk 安装包（前提是环境正确搭建）。

## 接口文档

- 运行服务后，可在 `/api/docs` 查看交互式接口文档。

- OpenAPI JSON 位于 `/api/openapi.json`。

- WebSocket 状态推送地址为 `/api/v1/ws/status`，OpenAPI 不覆盖该接口；消息包含 `temperature`（温度）、`fan_speed`（转速）与 `source`（温度源：`cpu` 或 `hdd`）字段。

## 前端接口代码生成

后端接口变更后，按顺序执行以下命令更新前端客户端：

```bash
uv run --directory src python scripts/export_openapi.py
cd webui && npm run api:generate
```

生成的 `webui/openapi.json` 与 `webui/src/api/generated` 需随接口变更一起提交更新。

## 温度设置

配置文件 `[temperature]` 段用于控制温度采集：

- ```source = "cpu" | "hdd"```：温度源，默认 `cpu`。

- ```interval```：采集周期（秒），取值范围 1–60，默认 `1`。

硬盘温度优先通过 `smartctl` 读取，失败时回退到 sysfs 的 `drivetemp` 传感器。

# U-Fanctl 万由NAS风扇控制
![技术栈](https://img.shields.io/badge/%E5%89%8D%E7%AB%AF-Python_+_Vue3_+_Vite-brightgreen?style=flat-square)
![开发工具](https://img.shields.io/badge/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7-WebStorm_+_Pycharm-blue?style=flat-square)
![许可证](https://img.shields.io/github/license/antonkomarev/github-profile-views-counter.svg?style=flat-square)

## 项目简介
这是一款为万由NAS（HS-201P）开发的风扇控制软件。众所周知，HS-201P自带的风扇满速运行时噪音较大，安装其他NAS系统后会默认满速运行。使用该软件后，可以手动设置温度曲线，实现自动调节风扇转速。

## 软件界面
![ControlView](https://github.com/Mrkinte/U-Fanctl/blob/main/Docs/ControlView.png?raw=true)

## 注意事项
- 默认密码：admin
- 默认端口：3233
- 通过i2c总线控制风扇，需要sudo权限。
- 适用于HS-201P
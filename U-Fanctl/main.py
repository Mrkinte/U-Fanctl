import time

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger

from services.fan_control import regulate_fan_speed, set_speed, init_fan_control
from services.web_service import web
from utils.config_manager import init_config, get_config
from utils.project import print_welcome

if __name__ == "__main__":
    print_welcome()
    logger.add("log.txt", rotation="1 MB")

    init_config("config.toml")
    config = get_config()

    scheduler = BackgroundScheduler()

    res = init_fan_control()
    if res:
        # 启动软件时满速启动风扇一次，避免堵转。
        set_speed(100)
        if config.get("control.manual"):
            time.sleep(1)
            set_speed(config.get("control.manual_speed"))
        scheduler.add_job(regulate_fan_speed, "interval", seconds=1)

    scheduler.start()

    web_port = config.get("system.web_port")
    if web_port is not None:
        uvicorn.run(web, host="0.0.0.0", port=web_port)

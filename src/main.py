import argparse

import uvicorn

from fanctl.app import create_app
from fanctl.core.config import get_config, init_config
from fanctl.core.logging import setup_logging
from fanctl.core.meta import print_welcome
from fanctl.core.paths import CONFIG_PATH
from fanctl.services import controller, scheduler

WEB_DEFAULT_PORT = 3233


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=None,
        help="指定访问端口 (默认: 使用配置文件或 3233)",
    )
    args = parser.parse_args()

    print_welcome()
    setup_logging()
    init_config(CONFIG_PATH)

    config = get_config()
    web_port = args.port
    if web_port is None:
        web_port = config.get("system.web_port") or WEB_DEFAULT_PORT

    if controller.initialize():
        scheduler.start()

    uvicorn.run(create_app(), host="0.0.0.0", port=web_port)


if __name__ == "__main__":
    main()

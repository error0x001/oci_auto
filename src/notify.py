from requests import RequestException, Session

from logger import logger


class Telegram:
    __FAILED_MESSAGE = "Message fail to sent via telegram"
    __DISABLED_TELEGRAM = "[TELEGRAM BOT IS DISABLED]"

    def __init__(self, bot_api: str, chat_id: str) -> None:
        self.__session = Session()
        self.__is_active = bool(bot_api and chat_id)
        self.bot_api = bot_api
        self.chat_id = chat_id

    def close(self) -> None:
        self.__session.close()

    def send(self, message: str) -> None:
        if not self.__is_active:
            logger.info(f"{self.__DISABLED_TELEGRAM} {message}")
            return
        try:
            self.__session.get(
                f"https://api.telegram.org/bot{self.bot_api}/sendMessage?chat_id={self.chat_id}&text={message}"
            )
        except RequestException:
            logger.error(self.__FAILED_MESSAGE)

import httpx

from src.logger import get_logger


logger = get_logger(__name__)


class HTTPXClientWrapper:
    async_client: None | httpx.AsyncClient = None

    def start(self):
        self.async_client = httpx.AsyncClient()
        logger.debug("httpx connection pool started !")

    async def stop(self):
        if self.async_client is not None:
            await self.async_client.aclose()
            self.async_client = None
            logger.debug("httpx connection pool stoped !")

    def __call__(self):
        # Ensure we don't use it if not started / running
        assert self.async_client is not None
        return self.async_client

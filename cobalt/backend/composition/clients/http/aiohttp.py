from application.contracts.loggers import AbstractLogger
from application.contracts.clients import AbstractHttpClient
from infrastructure.clients.http import AiohttpClient


def create_aiohttp_client(
    logger: AbstractLogger
) -> AbstractHttpClient:
    """
    Creates a Aiohttp client.

    Parameters:
    - logger: AbstractLogger object.

    Returns:
    - AbstractHttpClient: AbstractHttpClient object.
    """
    return AiohttpClient(
        logger=logger
    )

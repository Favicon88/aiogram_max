from __future__ import annotations

from ..types import User
from .base import MaxMethod


class GetMe(MaxMethod[User]):
    """
    A simple method for testing your bot's authentication token. Requires no parameters. Returns basic information about the bot in form of a :class:`aiogram.types.user.User` object.

    Source: https://dev.max.ru/docs-api/methods/GET/me
    """

    __returning__ = User
    __api_method__ = "me"
    __http_method__ = "GET"

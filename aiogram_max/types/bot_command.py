from __future__ import annotations
from pydantic import Field
from typing import TYPE_CHECKING, Any

from .base import MutableTelegramObject


class BotCommand(MutableTelegramObject):
    """
    This object represents a bot command.

    Source: https://dev.max.ru/docs-api/objects/BotCommand
    """

    name: str = Field(..., alias="command")
    """Text of the command; 1-32 characters. Can contain only lowercase English letters, digits and underscores."""
    description: str
    """Description of the command; 1-256 characters."""

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            command: str,  # Используем 'command' для удобства aiogram
            description: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                command=command, description=description, **__pydantic_kwargs
            )

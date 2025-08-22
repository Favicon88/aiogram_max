from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
from ..types import UpdatesResponse
from .base import MaxMethod
from pydantic import Field


class GetUpdates(MaxMethod[UpdatesResponse]):
    """
    Use this method to receive incoming updates using long polling (`wiki <https://en.wikipedia.org/wiki/Push_technology#Long_polling>`_). Returns an Array of :class:`aiogram.types.update.Update` objects.

     **Notes**

     **1.** This method will not work if an outgoing webhook is set up.

     **2.** In order to avoid getting duplicate updates, recalculate *offset* after each server response.

    Source: https://dev.max.ru/docs-api/objects/Update
    """

    __returning__ = UpdatesResponse
    __api_method__ = "updates"
    __http_method__ = "GET"

    limit: Optional[int] = Field(
        None,
        description="Максимальное количество обновлений для получения. По умолчанию: 100",
    )
    timeout: Optional[int] = Field(
        None,
        description="По умолчанию: 100 Максимальное количество обновлений для получения",
    )
    marker: Optional[int] = Field(
        None,
        description="Если передан, бот получит обновления, которые еще не были получены. Если не передан, получит все новые обновления",
    )
    types: Optional[list[str]] = Field(
        None,
        description="Пример: types=message_created,message_callback Список типов обновлений, которые бот хочет получить (например, message_created, message_callback)я",
    )

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            limit: Optional[int] = None,
            timeout: Optional[int] = None,
            marker: Optional[int] = None,
            types: Optional[list[str]] = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(
                limit=limit,
                timeout=timeout,
                marker=marker,
                types=types,
                **__pydantic_kwargs,
            )

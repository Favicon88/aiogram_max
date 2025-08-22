from __future__ import annotations
from typing import List, Union
from typing import Optional
from pydantic import BaseModel, Field
from ..types import BotCommand


class MeResponse(BaseModel):
    user_id: int = Field(..., description="ID пользователя")
    first_name: str = Field(..., description="Отображаемое имя пользователя")
    last_name: Optional[str] = Field(
        None, description="Отображаемое имя пользователя"
    )
    name: Optional[str] = Field(
        None, description="Устаревшее поле, скоро будет удалено"
    )
    username: Optional[str] = Field(
        None,
        description="Уникальное публичное имя пользователя. Может быть null, если пользователь недоступен или имя не задано",
    )
    is_bot: bool = Field(
        ..., description="true, если пользователь является ботом"
    )
    last_activity_time: int = Field(
        ...,
        description="Время последней активности пользователя в MAX (Unix-время в миллисекундах). Может быть неактуальным, если пользователь отключил статус онлайн в настройках.",
    )
    description: Optional[str] = Field(
        None,
        description="до 16000 символов Описание пользователя. Может быть null, если пользователь его не заполнил",
    )
    avatar_url: Optional[str] = Field(None, description="URL аватара")
    full_avatar_url: Optional[str] = Field(
        None, description="URL аватара большего размера"
    )
    commands: Optional[List[BotCommand]] = Field(
        None, description="до 32 элементов Команды, поддерживаемые ботом"
    )

    model_config = {"extra": "ignore"}

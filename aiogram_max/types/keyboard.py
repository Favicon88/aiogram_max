from pydantic import BaseModel
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, Literal
from enum import Enum


class Intent(str, Enum):
    """
    По умолчанию: "default"
    Enum: "positive" "negative" "default"

    Намерение кнопки. Влияет на отображение клиентом.
    """

    default = "default"
    positive = "positive"
    negative = "negative"


class ButtonBase(BaseModel):
    type: str  # discriminator, но будет конкретизирован в наследниках


class CallbackButton(ButtonBase):
    type: Literal["callback"]
    text: str
    """от 1 до 128 символов. Видимый текст кнопки."""
    payload: str
    """до 1024 символов. Токен кнопки"""
    intent: Optional[Intent] = "default"
    """По умолчанию: "default" Enum: "positive" "negative" "default" Намерение кнопки. Влияет на отображение клиентом."""


class LinkButton(ButtonBase):
    type: Literal["link"]
    text: str
    """от 1 до 128 символов. Видимый текст кнопки."""
    url: str
    """до 2048 символов"""


class RequestGeoLocationButton(ButtonBase):
    type: Literal["request_geo_location"]
    text: str
    """от 1 до 128 символов. Видимый текст кнопки."""
    quick: Optional[bool] = True
    """Если true, отправляет местоположение без запроса подтверждения пользователя"""


class RequestContactButton(ButtonBase):
    type: Literal["request_contact"]
    text: str
    """от 1 до 128 символов. Видимый текст кнопки."""


class OpenAppButton(ButtonBase):
    type: Literal["open_app"]
    text: str
    """от 1 до 128 символов. Видимый текст кнопки."""
    web_app: Optional[str]
    """Публичное имя (username) бота или ссылка на него, чьё мини-приложение надо запустить."""
    contact_id: Optional[int]
    """Идентификатор бота, чьё мини-приложение надо запустить."""


class MessageButton(ButtonBase):
    type: Literal["message"]
    text: str
    """от 1 до 128 символов Текст кнопки, который будет отправлен в чат от лица пользователя."""


TypeButton = Union[
    CallbackButton,
    LinkButton,
    RequestGeoLocationButton,
    RequestContactButton,
    OpenAppButton,
    MessageButton,
]


class Keyboard(BaseModel):
    """Клавиатура - это двумерный массив кнопок."""

    buttons: List[TypeButton]

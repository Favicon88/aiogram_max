from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Dict, Literal

from .base import MutableTelegramObject
from .keyboard import (
    Keyboard,
    TypeButton,
    CallbackButton,
    LinkButton,
    RequestGeoLocationButton,
    RequestContactButton,
    OpenAppButton,
    MessageButton,
)
from .attachment import KeyboardAttachment

if TYPE_CHECKING:
    from .inline_keyboard_button import InlineKeyboardButton


# class InlineKeyboardMarkup(MutableTelegramObject):
#     """
#     This object represents an `inline keyboard <https://dev.max.ru/docs-api>`_ that appears right next to the message it belongs to.

#     Source: https://dev.max.ru/docs-api
#     """

#     inline_keyboard: list[list[InlineKeyboardButton]]
#     """Array of button rows, each represented by an Array of :class:`aiogram.types.inline_keyboard_button.InlineKeyboardButton` objects"""

#     if TYPE_CHECKING:

#         def __init__(
#             __pydantic__self__,
#             *,
#             inline_keyboard: list[list[InlineKeyboardButton]],
#             **__pydantic_kwargs: Any,
#         ) -> None:
#             super().__init__(
#                 inline_keyboard=inline_keyboard, **__pydantic_kwargs
#             )


class InlineKeyboardMarkup(MutableTelegramObject):
    """
    This object represents an `inline keyboard <https://dev.max.ru/docs-api>`_ that appears right next to the message it belongs to.

    Source: https://dev.max.ru/docs-api
    """

    type: Literal["inline_keyboard"] = "inline_keyboard"

    inline_keyboard: list[list[InlineKeyboardButton]]
    """Array of button rows, each represented by an Array of :class:`aiogram.types.inline_keyboard_button.InlineKeyboardButton` objects"""

    def to_max_payload(self) -> Keyboard:
        """
        Преобразует InlineKeyboardMarkup в формат вложения для MAX API.
        """
        max_buttons: List[TypeButton] = []

        # Проходим по всем строкам
        for row in self.inline_keyboard:
            # Проходим по всем кнопкам в строке
            for button in row:
                if button.callback_data:
                    max_buttons.append(
                        CallbackButton(
                            text=button.text, payload=button.callback_data
                        )
                    )
                elif button.text and not any(
                    [
                        button.callback_data,
                        button.url,
                        button.web_app,
                        # ... другие типы кнопок, которые не MessageButton
                    ]
                ):
                    max_buttons.append(MessageButton(text=button.text))
                elif button.url:
                    max_buttons.append(
                        LinkButton(text=button.text, url=button.url)
                    )
                elif button.web_app:
                    # Это кнопка для запуска мини-приложения
                    # Предполагаем, что web_app имеет атрибут url
                    max_buttons.append(
                        OpenAppButton(
                            text=button.text, web_app=button.web_app.url
                        )
                    )
                # Добавьте здесь другие условия для других типов кнопок,
                # например, request_contact, request_geo_location, etc.

        return Keyboard(
            buttons=[
                max_buttons,
            ]
        )

    # Переопределяем model_dump для автоматической сериализации
    def model_dump(self, *args, **kwargs) -> List[str, Any]:
        """
        Переопределяет model_dump для создания вложения с клавиатурой.
        """
        # Создаем KeyboardAttachment, используя адаптированный payload
        keyboard_attachment = KeyboardAttachment(payload=self.to_max_payload())

        # Создаем список вложений
        attachments = [keyboard_attachment.model_dump(mode="json")]

        # Возвращаем словарь, который будет включать только `attachments`
        return attachments

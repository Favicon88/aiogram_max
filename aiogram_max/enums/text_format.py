from enum import Enum


class TextFormat(str, Enum):
    """
    Enum: "markdown" "html"

    Если установлен, текст сообщения будет форматрован данным способом.
    Для подробной информации загляните в раздел Форматирование
    """

    markdown = "markdown"
    html = "html"

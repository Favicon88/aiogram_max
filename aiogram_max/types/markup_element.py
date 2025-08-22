from pydantic import BaseModel, Field
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, Literal
from enum import Enum


class MarkupElement(BaseModel):
    """Разметка текста сообщения. Для подробной информации загляните в раздел Форматирование."""

    type: str  # discriminator, но будет конкретизирован в наследниках


class StrongMarkup(MarkupElement):
    type: Literal["strong"] = Field(
        description="Тип элемента разметки. Может быть жирный, курсив, зачеркнутый, подчеркнутый, моноширинный, ссылка или упоминание пользователя"
    )
    from_: int = Field(
        alias="from",
        description="Индекс начала элемента разметки в тексте. Нумерация с нуля",
    )
    length: int = Field(description="Длина элемента разметки")

    class Config:
        populate_by_name = True


class EmphasizedMarkup(MarkupElement):
    type: Literal["emphasized"] = Field(
        description="Тип элемента разметки. Может быть жирный, курсив, зачеркнутый, подчеркнутый, моноширинный, ссылка или упоминание пользователя"
    )
    from_: int = Field(
        alias="from",
        description="Индекс начала элемента разметки в тексте. Нумерация с нуля",
    )
    length: int = Field(description="Длина элемента разметки")

    class Config:
        populate_by_name = True


class MonospacesMarkup(MarkupElement):
    type: Literal["monospaced"] = Field(
        description="Тип элемента разметки. Может быть жирный, курсив, зачеркнутый, подчеркнутый, моноширинный, ссылка или упоминание пользователя"
    )
    from_: int = Field(
        alias="from",
        description="Индекс начала элемента разметки в тексте. Нумерация с нуля",
    )
    length: int = Field(description="Длина элемента разметки")

    class Config:
        populate_by_name = True


class LinkMarkup(MarkupElement):
    type: Literal["link"] = Field(
        description="Тип элемента разметки. Может быть жирный, курсив, зачеркнутый, подчеркнутый, моноширинный, ссылка или упоминание пользователя"
    )
    from_: int = Field(
        alias="from",
        description="Индекс начала элемента разметки в тексте. Нумерация с нуля",
    )
    length: int = Field(description="Длина элемента разметки")
    url: str = Field(description="от 1 до 2048 символов URL ссылки")

    class Config:
        populate_by_name = True


class StrikethroughMarkup(MarkupElement):
    type: Literal["strikethrough"] = Field(
        description="Тип элемента разметки. Может быть жирный, курсив, зачеркнутый, подчеркнутый, моноширинный, ссылка или упоминание пользователя"
    )
    from_: int = Field(
        alias="from",
        description="Индекс начала элемента разметки в тексте. Нумерация с нуля",
    )
    length: int = Field(description="Длина элемента разметки")

    class Config:
        populate_by_name = True


class UnderlinehMarkup(MarkupElement):
    type: Literal["underline"] = Field(
        description="Тип элемента разметки. Может быть жирный, курсив, зачеркнутый, подчеркнутый, моноширинный, ссылка или упоминание пользователя"
    )
    from_: int = Field(
        alias="from",
        description="Индекс начала элемента разметки в тексте. Нумерация с нуля",
    )
    length: int = Field(description="Длина элемента разметки")

    class Config:
        populate_by_name = True


class UserMentionhMarkup(MarkupElement):
    type: Literal["user_mention"] = Field(
        description="Тип элемента разметки. Может быть жирный, курсив, зачеркнутый, подчеркнутый, моноширинный, ссылка или упоминание пользователя"
    )
    from_: int = Field(
        alias="from",
        description="Индекс начала элемента разметки в тексте. Нумерация с нуля",
    )
    length: int = Field(description="Длина элемента разметки")
    user_link: Optional[str] = Field(
        None, description="@username упомянутого пользователя"
    )
    user_id: Optional[int] = Field(
        None, description="ID упомянутого пользователя без имени"
    )

    class Config:
        populate_by_name = True


class HeadingMarkup(MarkupElement):
    type: Literal["heading"] = Field(
        description="Тип элемента разметки. Может быть жирный, курсив, зачеркнутый, подчеркнутый, моноширинный, ссылка или упоминание пользователя"
    )
    from_: int = Field(
        alias="from",
        description="Индекс начала элемента разметки в тексте. Нумерация с нуля",
    )
    length: int = Field(description="Длина элемента разметки")

    class Config:
        populate_by_name = True


class HighlightedMarkup(MarkupElement):
    type: Literal["highlighted"] = Field(
        description="Тип элемента разметки. Может быть жирный, курсив, зачеркнутый, подчеркнутый, моноширинный, ссылка или упоминание пользователя"
    )
    from_: int = Field(
        alias="from",
        description="Индекс начала элемента разметки в тексте. Нумерация с нуля",
    )
    length: int = Field(description="Длина элемента разметки")

    class Config:
        populate_by_name = True


MarkupElement = Union[
    StrongMarkup,
    EmphasizedMarkup,
    MonospacesMarkup,
    LinkMarkup,
    StrikethroughMarkup,
    UnderlinehMarkup,
    UserMentionhMarkup,
    HeadingMarkup,
    HighlightedMarkup,
]

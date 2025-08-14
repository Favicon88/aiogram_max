from pydantic import BaseModel, Field
from typing import Optional
from .attachment_request import AttachmentRequest
from ..enums import MessageLinkType, TextFormat


class NewMessageLink(BaseModel):
    type: Optional[MessageLinkType]
    mid: str = Field(description="ID сообщения исходного сообщения")


class NewMessageBody(BaseModel):
    text: Optional[str] = Field(
        description="до 4000 символов Новый текст сообщения"
    )
    attachments: Optional[AttachmentRequest] = Field(
        description="Вложения сообщения. Если пусто, все вложения будут удалены"
    )
    link: Optional[NewMessageLink] = Field(description="Ссылка на сообщение")
    notify: Optional[bool] = Field(
        True,
        description="По умолчанию: true Если false, участники чата не будут уведомлены (по умолчанию true)",
    )
    format: Optional[TextFormat] = Field(description="Enum: 'markdown' 'html'")

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field
from .user import User
from .keyboard import InlineKeyboardAttachmentRequestPayload


class VideoThumbnail:
    """Миниатюра видео."""

    url: str
    """URL изображения."""


class AttachmentBase(BaseModel):
    type: str  # discriminator, но будет конкретизирован в наследниках


class PhotoAttachmentRequestPayload(BaseModel):
    url: Optional[str] = Field(
        None,
        description="от 1 символа Любой внешний URL изображения, которое вы хотите прикрепить",
    )
    token: Optional[str] = Field(
        None,
        description="Токен существующего вложения",
    )
    photos: Any = Field(
        description="Токены, полученные после загрузки изображений"
    )


class UploadedInfo(BaseModel):
    token: Optional[str] = Field(
        None,
        description="Токен — уникальный ID загруженного медиафайла",
    )


class FileAttachmentPayload(BaseModel):
    url: str
    """URL медиа-вложения. Для видео-вложения используйте метод getVideoAttachmentDetails, чтобы получить прямые ссылки."""
    token: str
    """Используйте token, если вы пытаетесь повторно использовать одно и то же вложение в другом сообщении."""


class ShareAttachmentPayload(BaseModel):
    url: Optional[str] = Field(
        description="от 1 символа URL, прикрепленный к сообщению в качестве предпросмотра медиа"
    )
    token: Optional[str] = Field(description="Токен вложения")


class StickerAttachmentRequestPayload(BaseModel):
    code: str = Field(
        description="Код стикера",
    )


class ContactAttachmentRequestPayload(BaseModel):
    name: Optional[str] = Field(
        None,
        description="Имя контакта",
    )
    contact_id: Optional[int] = Field(
        None,
        description="ID контакта, если он зарегистирован в MAX",
    )
    vcf_info: Optional[str] = Field(
        None,
        description="Полная информация о контакте в формате VCF",
    )
    vcf_phone: Optional[str] = Field(
        None,
        description="Телефон контакта в формате VCF",
    )


class ImageAttachment(AttachmentBase):
    type: Literal["image"] = Field(
        description="Запрос на прикрепление изображения (все поля являются взаимоисключающими)"
    )
    payload: PhotoAttachmentRequestPayload


class VideoAttachment(AttachmentBase):
    type: Literal["video"]
    payload: UploadedInfo = Field(
        description="Это информация, которую вы получите, как только аудио/видео будет загружено"
    )


class AudioAttachment(AttachmentBase):
    type: Literal["audio"]
    payload: UploadedInfo = Field(
        description="Это информация, которую вы получите, как только аудио/видео будет загружено"
    )


class FileAttachment(AttachmentBase):
    type: Literal["file"]
    payload: UploadedInfo = Field(
        description="Это информация, которую вы получите, как только аудио/видео будет загружено"
    )


class StickerAttachment(AttachmentBase):
    type: Literal["sticker"]
    payload: StickerAttachmentRequestPayload


class ContactAttachment(AttachmentBase):
    type: Literal["contact"]
    payload: ContactAttachmentRequestPayload


class KeyboardAttachment(AttachmentBase):
    type: Literal["inline_keyboard"]
    payload: InlineKeyboardAttachmentRequestPayload
    """Клавиатура - это двумерный массив кнопок."""


class LocationAttachment(AttachmentBase):
    type: Literal["location"]
    latitude: float = Field(description="Широта")
    longitude: float = Field(description="Долгота")


class ShareAttachment(AttachmentBase):
    type: Literal["share"]
    payload: ShareAttachmentPayload


AttachmentRequest = Union[
    ImageAttachment,
    VideoAttachment,
    AudioAttachment,
    FileAttachment,
    StickerAttachment,
    ContactAttachment,
    KeyboardAttachment,
    LocationAttachment,
    ShareAttachment,
]

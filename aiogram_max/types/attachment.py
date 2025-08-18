from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel
from .user import User
from .keyboard import Keyboard


class VideoThumbnail(BaseModel):
    """Миниатюра видео."""

    url: str
    """URL изображения."""


class AttachmentBase(BaseModel):
    type: str  # discriminator, но будет конкретизирован в наследниках


class PhotoAttachmentPayload(BaseModel):
    photo_id: int
    token: str
    url: str


class MediaAttachmentPayload(BaseModel):
    url: str
    """URL медиа-вложения. Для видео-вложения используйте метод getVideoAttachmentDetails, чтобы получить прямые ссылки."""
    token: str
    """Используйте token, если вы пытаетесь повторно использовать одно и то же вложение в другом сообщении."""


class FileAttachmentPayload(BaseModel):
    url: str
    """URL медиа-вложения. Для видео-вложения используйте метод getVideoAttachmentDetails, чтобы получить прямые ссылки."""
    token: str
    """Используйте token, если вы пытаетесь повторно использовать одно и то же вложение в другом сообщении."""


class StickerAttachmentPayload(BaseModel):
    url: str
    """URL медиа-вложения. Для видео-вложения используйте метод getVideoAttachmentDetails, чтобы получить прямые ссылки."""
    code: str
    """ID стикера."""


class ContactAttachmentPayload(BaseModel):
    vcf_info: Optional[str] = None
    """Информация о пользователе в формате VCF."""
    max_info: Optional[User]
    """Информация о пользователе."""


class ImageAttachment(AttachmentBase):
    type: Literal["image"]
    payload: PhotoAttachmentPayload


class VideoAttachment(AttachmentBase):
    type: Literal["video"]
    payload: MediaAttachmentPayload
    thumbnail: Optional[VideoThumbnail] = None
    width: Optional[int] = None
    """Ширина видео."""
    height: Optional[int] = None
    """Высота видео."""
    duration: Optional[int] = None
    """Длина видео в секундах."""


class AudioAttachment(AttachmentBase):
    type: Literal["audio"]
    payload: MediaAttachmentPayload
    transcription: Optional[str]
    """Аудио транскрипция."""


class FileAttachment(AttachmentBase):
    type: Literal["file"]
    payload: FileAttachmentPayload
    filename: str
    """Имя загруженного файла."""
    size: int
    """Размер файла в байтах."""


class StickerAttachment(AttachmentBase):
    type: Literal["sticker"]
    payload: StickerAttachmentPayload
    width: int
    """Ширина стикера."""
    height: int
    """Высота стикера."""


class ContactAttachment(AttachmentBase):
    type: Literal["contact"]
    payload: ContactAttachmentPayload


class KeyboardAttachment(AttachmentBase):
    type: Literal["inline_keyboard"] = "inline_keyboard"
    payload: Keyboard
    """Клавиатура - это двумерный массив кнопок."""


Attachment = Union[
    ImageAttachment,
    VideoAttachment,
    AudioAttachment,
    FileAttachment,
    StickerAttachment,
    ContactAttachment,
    KeyboardAttachment,
]

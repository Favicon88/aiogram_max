from enum import Enum
from pydantic import Field


class ChatStatus(str, Enum):
    active = Field(
        "active", description="Бот является активным участником чата."
    )
    removed = Field("removed", description="Бот был удалён из чата.")
    left = Field("left", description="Бот покинул чат.")
    closed = Field("closed", description="Чат был закрыт.")

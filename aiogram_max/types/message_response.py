from .message import Message
from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: Message

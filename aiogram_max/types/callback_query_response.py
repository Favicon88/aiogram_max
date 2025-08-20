from .message import Message
from pydantic import BaseModel


class CallbackQueryResponse(BaseModel):
    success: bool
    message: Message

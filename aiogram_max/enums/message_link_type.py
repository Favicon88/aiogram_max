from enum import Enum


class MessageLinkType(str, Enum):
    """
    Enum: "forward" "reply"

    Тип связанного сообщения
    """

    forward = "forward"
    reply = "reply"

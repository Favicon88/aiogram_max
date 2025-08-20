from enum import Enum


class Intent(str, Enum):
    """
    По умолчанию: "default"
    Enum: "positive" "negative" "default"

    Намерение кнопки. Влияет на отображение клиентом.
    """

    default = "default"
    positive = "positive"
    negative = "negative"

from abc import ABC

from aiogram_max.handlers import BaseHandler
from aiogram_max.types import PreCheckoutQuery, User


class PreCheckoutQueryHandler(BaseHandler[PreCheckoutQuery], ABC):
    """
    Base class for pre-checkout handlers
    """

    @property
    def from_user(self) -> User:
        return self.event.from_user

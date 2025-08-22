from abc import ABC

from aiogram_max.handlers import BaseHandler
from aiogram_max.types import ShippingQuery, User


class ShippingQueryHandler(BaseHandler[ShippingQuery], ABC):
    """
    Base class for shipping query handlers
    """

    @property
    def from_user(self) -> User:
        return self.event.from_user

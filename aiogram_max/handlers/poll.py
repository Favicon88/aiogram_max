from abc import ABC
from typing import List

from aiogram_max.handlers import BaseHandler
from aiogram_max.types import Poll, PollOption


class PollHandler(BaseHandler[Poll], ABC):
    """
    Base class for poll handlers
    """

    @property
    def question(self) -> str:
        return self.event.question

    @property
    def options(self) -> List[PollOption]:
        return self.event.options

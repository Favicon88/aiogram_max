from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from ..utils import markdown
from ..utils.link import create_tg_link
from .base import TelegramObject
from pydantic import Field

if TYPE_CHECKING:
    from ..methods import GetUserProfilePhotos


class User(TelegramObject):
    """
    This object represents a Max user or bot.

    Source: https://dev.max.ru/docs-api/objects/User
    """

    user_id: int
    """ID пользователя"""
    first_name: str
    """Отображаемое имя пользователя"""
    last_name: Optional[str] = None
    """Отображаемая фамилия пользователя"""
    name: Optional[str] = None
    """Устаревшее поле, скоро будет удалено"""
    username: Optional[str] = None
    """Уникальное публичное имя пользователя. Может быть null, если пользователь недоступен или имя не задано"""
    is_bot: bool
    """:code:`True`, if this user is a bot"""
    last_activity_time: int
    """Время последней активности пользователя в MAX (Unix-время в миллисекундах). Может быть неактуальным, если пользователь отключил статус "онлайн" в настройках."""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            user_id: int,
            is_bot: bool,
            first_name: str,
            last_name: Optional[str] = None,
            name: Optional[str] = None,
            username: Optional[str] = None,
            last_activity_time: int,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(
                user_id=user_id,
                is_bot=is_bot,
                first_name=first_name,
                last_name=last_name,
                name=name,
                username=username,
                last_activity_time=last_activity_time,
                **__pydantic_kwargs,
            )

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.user_id)

    def mention_markdown(self, name: Optional[str] = None) -> str:
        if name is None:
            name = self.full_name
        return markdown.link(name, self.url)

    def mention_html(self, name: Optional[str] = None) -> str:
        if name is None:
            name = self.full_name
        return markdown.hlink(name, self.url)

    def get_profile_photos(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs: Any,
    ) -> GetUserProfilePhotos:
        """
        Shortcut for method :class:`aiogram.methods.get_user_profile_photos.GetUserProfilePhotos`
        will automatically fill method attributes:

        - :code:`user_id`

        Use this method to get a list of profile pictures for a user. Returns a :class:`aiogram.types.user_profile_photos.UserProfilePhotos` object.

        Source: https://core.telegram.org/bots/api#getuserprofilephotos

        :param offset: Sequential number of the first photo to be returned. By default, all photos are returned.
        :param limit: Limits the number of photos to be retrieved. Values between 1-100 are accepted. Defaults to 100.
        :return: instance of method :class:`aiogram.methods.get_user_profile_photos.GetUserProfilePhotos`
        """
        # DO NOT EDIT MANUALLY!!!
        # This method was auto-generated via `butcher`

        from aiogram_max.methods import GetUserProfilePhotos

        return GetUserProfilePhotos(
            user_id=self.user_id,
            offset=offset,
            limit=limit,
            **kwargs,
        ).as_(self._bot)


class UserWithPhoto(User):
    description: Optional[str] = Field(
        description="до 16000 символов Описание пользователя. Может быть null, если пользователь его не заполнил"
    )
    avatar_url: Optional[str] = Field(description="URL аватара")
    full_avatar_url: Optional[str] = Field(description="URL аватара")

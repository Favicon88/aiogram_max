from __future__ import annotations

import asyncio
import ssl
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    Union,
    cast,
)

import certifi
from aiohttp import (
    BasicAuth,
    ClientError,
    ClientSession,
    FormData,
    TCPConnector,
)
from aiohttp.hdrs import USER_AGENT
from aiohttp.http import SERVER_SOFTWARE

from aiogram_max.__meta__ import __version__
from aiogram_max.methods import MaxMethod
from aiogram_max.methods.send_message import SendMessage

from ...exceptions import TelegramNetworkError
from ...methods.base import TelegramType
from ...types import InputFile
from .base import BaseSession

if TYPE_CHECKING:
    from ..bot import Bot

_ProxyBasic = Union[str, Tuple[str, BasicAuth]]
_ProxyChain = Iterable[_ProxyBasic]
_ProxyType = Union[_ProxyChain, _ProxyBasic]


def _retrieve_basic(basic: _ProxyBasic) -> Dict[str, Any]:
    from aiohttp_socks.utils import parse_proxy_url

    proxy_auth: Optional[BasicAuth] = None

    if isinstance(basic, str):
        proxy_url = basic
    else:
        proxy_url, proxy_auth = basic

    proxy_type, host, port, username, password = parse_proxy_url(proxy_url)
    if isinstance(proxy_auth, BasicAuth):
        username = proxy_auth.login
        password = proxy_auth.password

    return {
        "proxy_type": proxy_type,
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "rdns": True,
    }


def _prepare_connector(
    chain_or_plain: _ProxyType,
) -> Tuple[Type["TCPConnector"], Dict[str, Any]]:
    from aiohttp_socks import ChainProxyConnector, ProxyConnector, ProxyInfo

    # since tuple is Iterable(compatible with _ProxyChain) object, we assume that
    # user wants chained proxies if tuple is a pair of string(url) and BasicAuth
    if isinstance(chain_or_plain, str) or (
        isinstance(chain_or_plain, tuple) and len(chain_or_plain) == 2
    ):
        chain_or_plain = cast(_ProxyBasic, chain_or_plain)
        return ProxyConnector, _retrieve_basic(chain_or_plain)

    chain_or_plain = cast(_ProxyChain, chain_or_plain)
    infos: List[ProxyInfo] = []
    for basic in chain_or_plain:
        infos.append(ProxyInfo(**_retrieve_basic(basic)))

    return ChainProxyConnector, {"proxy_infos": infos}


class AiohttpSession(BaseSession):
    def __init__(
        self,
        proxy: Optional[_ProxyType] = None,
        limit: int = 100,
        **kwargs: Any,
    ) -> None:
        """
        Client session based on aiohttp.

        :param proxy: The proxy to be used for requests. Default is None.
        :param limit: The total number of simultaneous connections. Default is 100.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)

        self._session: Optional[ClientSession] = None
        self._connector_type: Type[TCPConnector] = TCPConnector
        self._connector_init: Dict[str, Any] = {
            "ssl": ssl.create_default_context(cafile=certifi.where()),
            "limit": limit,
            "ttl_dns_cache": 3600,  # Workaround for https://github.com/aiogram/aiogram/issues/1500
        }
        self._should_reset_connector = True  # flag determines connector state
        self._proxy: Optional[_ProxyType] = None

        if proxy is not None:
            try:
                self._setup_proxy_connector(proxy)
            except ImportError as exc:  # pragma: no cover
                raise RuntimeError(
                    "In order to use aiohttp client for proxy requests, install "
                    "https://pypi.org/project/aiohttp-socks/"
                ) from exc

    def _setup_proxy_connector(self, proxy: _ProxyType) -> None:
        self._connector_type, self._connector_init = _prepare_connector(proxy)
        self._proxy = proxy

    @property
    def proxy(self) -> Optional[_ProxyType]:
        return self._proxy

    @proxy.setter
    def proxy(self, proxy: _ProxyType) -> None:
        self._setup_proxy_connector(proxy)
        self._should_reset_connector = True

    async def create_session(self) -> ClientSession:
        if self._should_reset_connector:
            await self.close()

        if self._session is None or self._session.closed:
            self._session = ClientSession(
                connector=self._connector_type(**self._connector_init),
                headers={
                    USER_AGENT: f"{SERVER_SOFTWARE} aiogram_max/{__version__}",
                },
            )
            self._should_reset_connector = False

        return self._session

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()

            # Wait 250 ms for the underlying SSL connections to close
            # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
            await asyncio.sleep(0.25)

    def build_form_data(
        self, bot: Bot, method: MaxMethod[TelegramType]
    ) -> FormData:
        if isinstance(method, SendMessage):
            payload: dict[str, Any] = {}

            if method.text is not None:
                payload["text"] = method.text

            if getattr(method, "attachments", None):
                # attachments — список Pydantic-моделей
                payload["attachments"] = [
                    att.model_dump(exclude_none=True)
                    for att in method.attachments
                ]

            if getattr(method, "link", None):
                # link — объект Pydantic-модели
                payload["link"] = method.link.model_dump(exclude_none=True)

            if getattr(method, "notify", None) is not None:
                payload["notify"] = method.notify

            if getattr(method, "format", None):
                payload["format"] = method.format

            return {"json": payload}
        else:
            form = FormData(quote_fields=False)
            files: Dict[str, InputFile] = {}
            for key, value in method.model_dump(warnings=False).items():
                value = self.prepare_value(value, bot=bot, files=files)
                if not value:
                    continue
                form.add_field(key, value)
            for key, value in files.items():
                form.add_field(
                    key,
                    value.read(bot),
                    filename=value.filename or key,
                )
        return form

    async def make_request(
        self,
        bot: Bot,
        method: MaxMethod[TelegramType],
        timeout: Optional[int] = None,
    ) -> TelegramType:
        session = await self.create_session()

        url = self.api.api_url(token=bot.token, method=method.__api_method__)
        form = self.build_form_data(bot=bot, method=method)

        http_method = getattr(method, "__http_method__", "POST").upper()
        request_method = getattr(session, http_method.lower(), None)

        if request_method is None:
            raise ValueError(f"Unsupported HTTP method: {http_method}")

        # Определяем, куда передавать данные
        kwargs = {
            "timeout": self.timeout if timeout is None else timeout,
        }
        if http_method in ("POST", "PATCH"):
            if isinstance(method, SendMessage):
                url += f"&chat_id={method.chat_id}"
                kwargs = form
            else:
                kwargs["data"] = form  # aiohttp сам примет FormData или dict
        elif http_method == "GET":
            # params должен быть только dict или последовательность пар
            if hasattr(form, "items"):
                kwargs["params"] = dict(form)
        else:
            raise TypeError(
                "GET request requires form to be a dict-like object"
            )

        try:
            async with request_method(url, **kwargs) as resp:
                raw_result = await resp.text()
        except asyncio.TimeoutError:
            raise TelegramNetworkError(
                method=method, message="Request timeout error"
            )
        except ClientError as e:
            raise TelegramNetworkError(
                method=method, message=f"{type(e).__name__}: {e}"
            )
        response = self.check_response(
            bot=bot, method=method, status_code=resp.status, content=raw_result
        )
        return cast(TelegramType, response)

    async def stream_content(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:
        if headers is None:
            headers = {}

        session = await self.create_session()

        async with session.get(
            url,
            timeout=timeout,
            headers=headers,
            raise_for_status=raise_for_status,
        ) as resp:
            async for chunk in resp.content.iter_chunked(chunk_size):
                yield chunk

    async def __aenter__(self) -> AiohttpSession:
        await self.create_session()
        return self

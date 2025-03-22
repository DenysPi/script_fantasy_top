from curl_cffi import requests

from config import config
class BaseAsyncSession(requests.AsyncSession):
    def __init__(self, proxy: str | None,
                 user_agent = config.DEFAULT_USER_AGENT,
                 *,
                 impersonate: requests.BrowserType = requests.BrowserType.chrome131,
                 **kwargs
        ):
        
        proxies = {"http": proxy, "https": proxy}
        headers = kwargs.pop("headers", {})
        headers["user-agent"] = user_agent
        super().__init__(
            proxies=proxies,
            headers=headers,
            impersonate=impersonate,
            **kwargs,
        )
        
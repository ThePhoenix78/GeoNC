import threading
import requests
import aiohttp
import asyncio
import time


class APIResponse:
    def __init__(self, headers: dict, json: dict, text: str, content: bytes, status_code: int, is_cache: bool):
        self.headers: dict = headers
        self.json: dict = json
        self.text: str = text
        self.content: bytes = content
        self.status_code: int = status_code
        self.is_cache: bool = is_cache


class GeoRequests():
    def __init__(self, base_url: str, use_etag: bool = True):
        self.base_api: str = base_url

        self.session: requests.Session = requests.Session()

        self.headers: dict = {}
        self.payload: str = ""

        self.cache: dict = {}
        self.etag: dict = {}

        self.use_etag: bool = use_etag

        self._run: bool = False
        self._refresh: int = 60

        self._to_call: dict = {}
        self.waiting_list: list = []

    def close_session(self):
        self.session.close()

    """
    REQUESTS SYNC
    """

    def request(self, method: str = "GET", endpoint: str = "", headers: dict = None, payload: str = None, etag: str = None, use_cache: bool = False, *args, **kwargs):
        if method.upper() not in ["GET", "HEAD", "OPTIONS", "TRACE", "PUT", "DELETE", "POST", "PATCH", "CONNECT"]:
            endpoint: str = method
            method: str = "GET"

        if not endpoint.startswith("/"):
            endpoint: str = f"/{endpoint}"

        if headers is None:
            headers: dict = self.headers

        if payload is None:
            payload: str = self.payload

        if use_cache:
            cached_data = self.cache.get(endpoint)

            if cached_data is not None:
                return APIResponse(headers={}, json=cached_data.get("json"), text=cached_data.get("text"), status_code=None, is_cache=True)

        _headers: dict = {}

        if self.use_etag:
            _headers: dict = {"If-None-Match": etag} if etag is not None else {"If-None-Match": self.etag.get(endpoint)}

            if self.etag.get(endpoint) is None or etag == "":
                _headers: dict = {"etag": ""}

        headers: dict = {**headers, **_headers}

        with self.session.request(method=method, url=f"{self.base_api}{endpoint}", headers=headers, data=payload, *args, **kwargs) as data:
            if data.status_code == 200:
                try:
                    data_json: dict = data.json()
                except Exception:
                    data_json: str = {}

                if self.use_etag:
                    self.etag[endpoint] = data.headers.get("etag", self.etag.get(endpoint))
                    self.cache[endpoint] = {"json": data_json, "text": data.text, "content": data.content}
    
                return APIResponse(headers=data.headers, json=data_json, text=data.text, content=data.content, status_code=data.status_code, is_cache=False)

            elif data.status_code == 304 and self.use_etag:
                cache: dict = self.cache.get(endpoint)
                return APIResponse(headers=data.headers, json=cache.get("json"), text=cache.get("text"), content=cache.get("content"), status_code=data.status_code, is_cache=True)

            return APIResponse(headers=data.headers, json={}, text=data.text, content=data.content, status_code=data.status_code, is_cache=False)

    def headers(self, endpoint: str, headers: dict = {}, payload: str = "", *args, **kwargs):
        with self.session.head(f"{self.base_api}{endpoint}", headers=headers, data=payload, *args, **kwargs) as data:
            return data

    """
    REQUESTS ASYNC
    """

    async def arequest(self, method: str = "GET", endpoint: str = "", headers: dict = None, payload: str = None, etag: str = None, use_cache: bool = False, session: aiohttp.ClientSession = None, *args, **kwargs):
        if method.upper() not in ["GET", "HEAD", "OPTIONS", "TRACE", "PUT", "DELETE", "POST", "PATCH", "CONNECT"]:
            endpoint: str = method
            method: str = "GET"

        if not endpoint.startswith("/"):
            endpoint: str = f"/{endpoint}"

        if headers is None:
            headers: dict = self.headers

        if payload is None:
            payload: str = self.payload

        if use_cache:
            cached_data = self.cache.get(endpoint)

            if cached_data is not None:
                return APIResponse(headers={}, json=cached_data.get("json"), text=cached_data.get("text"), status_code=None, is_cache=True)

        _headers: dict = {}

        if self.use_etag:
            _headers: dict = {"If-None-Match": etag} if etag is not None else {"If-None-Match": self.etag.get(endpoint)}

            if self.etag.get(endpoint) is None or etag == "":
                _headers: dict = {"etag": ""}

        headers: dict = {**headers, **_headers}

        data_json: dict = {}
        data_content: bytes = b""

        if session is None:
            async with aiohttp.ClientSession(base_url=self.base_api) as session:
                async with session.request(method=method, url=f"{endpoint}", headers=headers, data=payload, *args, **kwargs) as data:
    
                    if data.status == 200:
                        try:
                            data_json: dict = await data.json()
                        except Exception:
                            data_json: dict = {}

                        try:
                            data_content: bytes = await data.read()
                        except Exception:
                            data_content: bytes = b""

                        if self.use_etag:
                            self.etag[endpoint] = data.headers.get("etag", self.etag.get(endpoint))
                            self.cache[endpoint] = {"json": data_json, "text": data.text, "content": data_content}
    
                        return APIResponse(headers=data.headers, json=data_json, text=data.text, content=data_content, status_code=data.status, is_cache=False)

                    elif data.status == 304:
                        cache: dict = self.cache.get(endpoint)
                        return APIResponse(headers=data.headers, json=cache.get("json"), text=cache.get("text"), content=cache.get("content"), status_code=data.status, is_cache=True)

                    return APIResponse(headers=data.headers, json=data_json, text=data.text, content=data_content, status_code=data.status, is_cache=False)

        else:
            async with session.request(method=method, url=f"{self.base_api}{endpoint}", headers=headers, data=payload, *args, **kwargs) as data:
                # head: dict = await data.headers
                if data.status == 200:
                    try:
                        data_json: dict = await data.json()
                    except Exception:
                        data_json: str = {}

                    try:
                        data_content: bytes = await data.read()
                    except Exception:
                        data_content: bytes = b""

                    if self.use_etag:
                        self.etag[endpoint] = data.headers.get("etag", self.etag.get(endpoint))
                        self.cache[endpoint] = {"json": data_json, "text": data.text, "content": data_content}
                    
                    return APIResponse(headers=data.headers, json=data_json, text=data.text, content=data_content, status_code=data.status, is_cache=False)

                elif data.status == 304 and self.use_etag:
                    cache: dict = self.cache.get(endpoint)
                    return APIResponse(headers=data.headers, json=cache.get("json"), text=cache.get("text"), content=cache.get("content"), status_code=data.status, is_cache=True)

                return APIResponse(headers=data.headers, json=data_json, text=data.text, content=data_content, status_code=data.status, is_cache=False)


    async def aheaders(self, endpoint: str, headers: dict = {}, payload: str = "", session: aiohttp.ClientSession = None, *args, **kwargs):
        if session is None:
            async with aiohttp.ClientSession(base_url=self.base_api) as session:
                async with session.head(f"{endpoint}", headers=headers, data=payload, *args, **kwargs) as data:
                    return data
        else:
            async with session.head(f"{self.base_api}{endpoint}", headers=headers, data=payload, *args, **kwargs) as data:
                return data            
    """
    CRAWLER ASYNC
    """

    async def _listener(self):
        await asyncio.sleep(.1)

        while self._run:
            for url, dico in self._to_call.items():
                data = self.request(endpoint=url, headers=dico.get("headers", {}), payload=dico.get("payload"))

                if data.is_cache == False:
                    self.waiting_list.append([dico.get("callback"), data])

            await self.run_task()
            await asyncio.sleep(self._refresh)

    """
    CRAWLER SYNC
    """

    def _listener_sync(self):
        time.sleep(.1)

        while self._run:
            for url, dico in self._to_call.items():
                data: int = self.request(endpoint=url, headers=dico.get("headers", {}), payload=dico.get("payload"))

                if data.is_cache == False:
                    dico.get("callback")(data)

            time.sleep(self._refresh)

    def _check_listener(self, run_async: bool = True):
        if not self._run:
            self._run: bool = True
            # threading.Thread(target=self._listener).start()
            if run_async:
                self.start_async_thread(self._listener())
            else:
                threading.Thread(target=self._listener_sync).start()
            # threading.Thread(target=self.start_async_thread).start()

    """
    ASYNC TOOLS
    """
    def add_task(self, function: callable, args: list|dict|str = "no_args"):
        self.waiting_list.append([function, args])

    async def run_task(self):
        tasks: list = []
        answers: list = []

        for function, args in self.waiting_list:
            if args == "no_args":
                tasks.append([asyncio.create_task(function()), function, args])

            elif isinstance(args, list):
                tasks.append([asyncio.create_task(function(*args)), function, args])

            elif isinstance(args, dict):
                tasks.append([asyncio.create_task(function(**args)), function, args])

            else:
                tasks.append([asyncio.create_task(function(args)), function, args])

        for task, function, args in tasks:
            answers.append({"result": await task, "function": function, "args": args})

        tasks.clear()

        self.waiting_list.clear()
        self.waiting_list: list = []
        return answers

    def run_task_sync(self, thread: bool = False):
        if thread:
            threading.Thread(target=self._exec).start()
        else:
            return asyncio.run(self.run_task())

    def _exec(self):
        return asyncio.run(self.run_task())

    def start_async_thread(self, awaitable):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        threading.Thread(target=loop.run_forever).start()
        asyncio.run_coroutine_threadsafe(awaitable, loop)
        return loop

    def stop_async_thread(self, loop):
        loop.call_soon_threadsafe(loop.stop)

    """
    EVENT WRAPPER

    def on_api_update(self, callback: callable = None, endpoints: list = None, headers: dict = {}, payload: str = "", *args, **kwargs):
        if (isinstance(callback, str) or isinstance(callback, list)) and endpoints is None:
            endpoints: list = callback
            callback: callable = None

        if isinstance(endpoints, str):
            endpoints: list = [endpoints]

        def add_debug(func):
            self._check_listener(asyncio.iscoroutinefunction(func))

            for endpoint in endpoints:
                self._to_call[endpoint] = {"callback": func, "headers": headers, "payload": payload}

            return func

        if callable(callback):
            return add_debug(callback)

        return add_debug
    """
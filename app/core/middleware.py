import time
import json
import logging
from starlette.types import ASGIApp, Receive, Scope, Send, Message

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    """
    纯 ASGI 中间件，不继承 BaseHTTPMiddleware。
    这样做是为了不缓冲 StreamingResponse，保证 SSE 真正流式。
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        # 只处理 HTTP 请求（跳过 lifespan、websocket）
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # 跳过 CORS 预检，避免日志噪音
        if scope["method"] == "OPTIONS":
            await self.app(scope, receive, send)
            return

        start_time = time.time()
        method = scope["method"]
        path = scope["path"]

        # 缓存请求体，让下游路由仍能读到
        body_chunks = []

        async def wrapped_receive() -> Message:
            message = await receive()
            if message["type"] == "http.request":
                body_chunks.append(message.get("body", b""))
            return message

        # 拦截响应头，用于记录状态码。注意：不做任何缓冲，立即转发
        status_holder = {"status": None}

        async def wrapped_send(message: Message):
            if message["type"] == "http.response.start":
                status_holder["status"] = message["status"]
            await send(message)  # 立即转发，不缓冲 —— 这就是流式的关键

        try:
            await self.app(scope, wrapped_receive, wrapped_send)
        finally:
            elapsed_ms = (time.time() - start_time) * 1000
            raw_body = b"".join(body_chunks)
            log_body = self._desensitize(raw_body)
            logger.info(
                f"{method} {path} | 请求体: {log_body} | "
                f"状态码: {status_holder['status']} | 耗时: {elapsed_ms:.2f}ms"
            )

    @staticmethod
    def _desensitize(body: bytes) -> str:
        if not body:
            return "[空请求体]"
        try:
            json_body = json.loads(body.decode("utf-8"))
            if "prompt" in json_body and isinstance(json_body["prompt"], str):
                prompt = json_body["prompt"]
                if len(prompt) > 50:
                    json_body["prompt"] = prompt[:50] + "...(truncated)"
            return json.dumps(json_body, ensure_ascii=False)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return "[非JSON或二进制数据]"
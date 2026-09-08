import time
import json
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__) # 获取当前模块的日志器

class LoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件：记录每个 HTTP 请求的方法、路径、请求体、状态码和耗时"""
    async def dispatch(self, request: Request, call_next):
        # 记录请求开始时间，用于计算处理耗时
        start_time = time.time()
        # 获取请求方法（GET/POST/PUT/DELETE 等）
        method = request.method
        # 获取请求路径（如 /api/v1/chat），不含查询参数
        path = request.url.path

        # 读取请求体（缓存以便后续路由读取）
        body = await request.body()
        request._body = body

        # 脱敏处理
        log_body = None
        #如果请求体不为空
        if body:
            try:
                # 将请求体 bytes 解析为 JSON 字典，便于按字段名进行脱敏处理
                json_body = json.loads(body.decode('utf-8'))
                # 如果请求体中包含 "prompt" 字段且为字符串类型，则进行长度截断
                if "prompt" in json_body and isinstance(json_body["prompt"], str):
                    prompt = json_body["prompt"]
                    if len(prompt) > 50:
                        # 截断过长的 prompt，保留前 50 个字符并追加截断标记
                        json_body["prompt"] = prompt[:50] + "...(truncated)"
                # 将脱敏后的字典重新序列化为 JSON 字符串（ensure_ascii=False 保证中文可读）
                log_body = json.dumps(json_body, ensure_ascii=False)
            except (json.JSONDecodeError, UnicodeDecodeError):
                # 解析失败（非 JSON 格式或二进制数据），使用占位符代替
                log_body = "[非JSON或二进制数据]"
        else:
            # 请求体为空，使用占位符标记
            log_body = "[空请求体]"

        # 处理请求
        response = await call_next(request)
        # 计算耗时
        process_time_ms = (time.time() - start_time) * 1000
        logger.info(
            f"{method} {path} | 请求体: {log_body} | "
            f"状态码: {response.status_code} | 耗时: {process_time_ms:.2f}ms"
        )

        return response
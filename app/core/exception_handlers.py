from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import BizException
from app.models.response import APIResponse
import logging

# 获取当前模块的日志器，在 app.core.exception_handlers 模块中，它的值是 "app.core.exception_handlers"作为日志记录器的名称
logger = logging.getLogger(__name__)

async def biz_exception_handler(request: Request, exc: BizException):
    logger.warning(f"业务异常捕获 | 路径：{request.url.path} | 错误码：{exc.code} | 消息：{exc.message}")

    # 返回 JSON 响应
    return JSONResponse(
        status_code = exc.code, ## 业务异常仍返回 200，由调用方通过 code 判断
        content = APIResponse(code = exc.code, message = exc.message, data = None).model_dump() # model_dump() 方法将模型实例转换为字典格式
    )

async def global_exception_handler(request: Request, exc: Exception):
    # type(exc).__name__ 获取异常类的名字（如 ValueError、KeyError）
    # exc_info=True 记录异常的详细信息，包括栈跟踪
    logger.error(f"系统异常 | 路径: {request.url.path} | 类型: {type(exc).__name__}", exc_info=True)
    # 返回 JSON 响应
    return JSONResponse(
        status_code=500,
        content=APIResponse(code=500, message="Internal Server Error", data=None).model_dump() # model_dump() 方法将模型实例转换为字典格式
    )
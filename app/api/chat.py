from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json
import logging
from app.models.schemas import ChatRequest,ChatResponse
from app.core.ai_client import chat_with_ai, chat_with_ai_stream
from app.core.exceptions import BizException

logger = logging.getLogger(__name__)

# 聊天路由
router = APIRouter(prefix = "/ai",tags = ["AI"])

@router.post("/chat",response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    聊天接口

    接收用户的聊天请求，经过参数校验和业务规则检查后，调用AI服务生成回复并返回。

    Args:
        request (ChatRequest): 聊天请求体，包含用户输入的 prompt 字段。

    Returns:
        ChatResponse: 聊天响应体，包含AI生成的回复内容。

    Raises:
        BizException: 当 prompt 为空或仅含空白时，抛出 code=40001 的业务异常；
                      当 prompt 中包含非法关键字 "error" 时，抛出 code=40002 的业务异常。
                      所有异常由全局异常处理器统一捕获并转换为 HTTP 响应。
    """
    # 1.参数校验，如果prompt为空或仅含空白，返回400错误码
    if not request.prompt or not request.prompt.strip():
        raise BizException(code=40001, message="prompt 不能为空")

    # 2. 模拟业务异常（用于演示全局捕获）
    if "error" in request.prompt.lower():
        raise BizException(code=40002, message="业务规则禁止：prompt 包含非法关键字 'error'")

    # 3. 调用 AI（任何异常直接抛出，由全局处理器捕获）
    reply = await chat_with_ai(request.prompt)
    # 将AI回复封装为响应模型返回
    return ChatResponse(reply=reply)

@router.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """
        聊天接口（流式响应）
        以 SSE (Server-Sent Events) 格式逐步返回 AI 的回复。
    """
    # 1. 参数校验（同非流式，但错误需通过 SSE 事件下发）
    if not request.prompt or not request.prompt.strip():
        # 注意：流式接口无法使用全局异常处理器，需要在这里手动处理
        async def error_stream():
            yield f"data:{json.dumps({'type': 'error', 'code': 40001, 'message': 'prompt 不能为空'})}\n\n"
        return StreamingResponse(error_stream(), media_type="text/event-stream")

    if "error" in request.prompt.lower():
        async def error_stream():
            yield f"data:{json.dumps({'type': 'error', 'code': 40002, 'message': '业务规则禁止：prompt 包含非法关键字 \'error\''})}\n\n"
        return StreamingResponse(error_stream(), media_type="text/event-stream")

    # 2. 构建流式生成器
    async def event_generator():
        try:
            async for delta in chat_with_ai_stream(request.prompt):
                # 将每个 delta 包装成 SSE 事件
                event_data = {"type": "message", "content": delta}
                yield f"data:{json.dumps(event_data, ensure_ascii=False)}\n\n"
        except Exception as e:
            # 流式过程中出现异常，无法更改 HTTP 状态码，只能发送错误事件
            logger.error(f"流式 AI 调用失败: {e}", exc_info=True)
            error_event = {"type": "error", "code": 500, "message": "AI 服务内部错误"}
            yield f"data:{json.dumps(error_event, ensure_ascii=False)}\n\n"
        finally:
            # 发送结束标记
            yield f"data:{json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

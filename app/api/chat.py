from fastapi import APIRouter
from app.models.schemas import ChatRequest,ChatResponse
from app.core.ai_client import chat_with_ai
from app.core.exceptions import BizException

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
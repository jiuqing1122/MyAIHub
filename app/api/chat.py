from fastapi import APIRouter,HTTPException
from app.models.schemas import ChatRequest,ChatResponse
from app.core.ai_client import chat_with_ai

# 聊天路由
router = APIRouter(prefix = "/ai",tags = ["AI"])

@router.post("/chat",response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """"
    聊天接口

    接收用户的聊天请求，调用AI服务生成回复并返回。

    Args:
        request (ChatRequest): 聊天请求体，包含用户输入的 prompt 字段。

    Returns:
        ChatResponse: 聊天响应体，包含AI生成的回复内容。

    Raises:
        HTTPException: 当 prompt 为空时返回 400 错误；
                       当AI服务调用失败时返回 500 错误。
    """
    #参数校验，如果prompt为空或仅含空白，返回400错误码
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400,detail="prompt不能为空")

    try:
        reply = await chat_with_ai(request.prompt)
        # 将AI回复封装为响应模型返回
        return ChatResponse(reply=reply)
    except Exception as e:
        # 暂时捕获所有异常并转为 500（第二阶段会使用全局异常处理器）
        # TODO: 这里可以记录日志（第二阶段统一处理）
        raise HTTPException(status_code=500,detail=f"AI service error: {str(e)}")

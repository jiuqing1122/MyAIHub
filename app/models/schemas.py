from pydantic import BaseModel

class ChatRequest(BaseModel):
    """
    聊天请求模型
    :param prompt: 用户输入
    """
    prompt: str


class ChatResponse(BaseModel):
    """
    聊天响应模型
    :param reply: AI 回复内容
    """
    reply: str

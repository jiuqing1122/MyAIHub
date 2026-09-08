from typing import Any,Optional
from pydantic import BaseModel

class APIResponse(BaseModel):
    """
    API 统一响应模型模块

    提供标准化的接口响应格式，包含：
    - code: 状态码
    - message: 提示信息
    - data: 返回数据（可选）
    """
    code: int
    message: str
    data: Optional[Any] = None
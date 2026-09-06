from openai import AsyncOpenAI
from app.core.config import settings

# 根据配置初始化对应的 AI 客户端
if settings.AI_SERVICE_TYPE == "ollama":
    # Ollama 也兼容 OpenAI API 格式，使用 Ollama 的 base_url
    client = AsyncOpenAI(
        api_key="ollama",  # Ollama 不需要 API Key，但 openai 库要求必须有值
        base_url=settings.OLLAMA_BASE_URL
    )
    current_model = settings.OLLAMA_MODEL
else:
    # 默认使用 DeepSeek
    client = AsyncOpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL
    )
    current_model = settings.AI_MODEL


async def chat_with_ai(prompt: str) -> str:
    """
    调用 AI 非流式聊天补全接口（支持 DeepSeek 和 Ollama）
    :param prompt: 用户输入
    :return: AI 回复内容
    """
    response = await client.chat.completions.create(
        model = current_model,
        messages = [{"role": "user", "content": prompt}],
        stream = False, # 非流式响应
    )
    # 提取回复内容
    return response.choices[0].message.content
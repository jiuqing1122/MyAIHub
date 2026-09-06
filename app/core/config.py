import os
from dotenv import load_dotenv

load_dotenv()  # 从.env文件中载入环境变量

# 定义配置类
class Settings:
    # DeepSeek 配置
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    
    # Ollama 配置
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
    
    # AI 服务类型选择：deepseek 或 ollama
    AI_SERVICE_TYPE: str = os.getenv("AI_SERVICE_TYPE", "deepseek")
    
    # 通用模型配置
    AI_MODEL: str = os.getenv("AI_MODEL", "deepseek-chat")

    # 校验必要的配置（仅当使用 DeepSeek 时需要 API Key）
    if AI_SERVICE_TYPE == "deepseek" and not DEEPSEEK_API_KEY:
        raise ValueError("使用 DeepSeek 时，DEEPSEEK_API_KEY 必须在环境变量中")

# 创建配置实例
settings = Settings()
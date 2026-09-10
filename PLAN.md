# 项目结构

```
fastapi-ai-service/
├── .env                          # 环境变量（DEEPSEEK_API_KEY等）
├── .gitignore
├── requirements.txt              # fastapi, uvicorn, python-dotenv, openai
├── run.py                        # 启动脚本（可选）
├── logs/                         # 运行时自动生成，存放日志文件
│   └── app.log
└── app/
    ├── __init__.py
    ├── main.py                   # 应用入口：注册中间件、异常处理器、路由
    ├── api/
    │   ├── __init__.py
    │   └── chat.py               # /ai/chat 路由，调用 AI 客户端，主动抛出 BizException
    ├── core/
    │   ├── __init__.py
    │   ├── config.py             # 配置类（您的版本，支持 DeepSeek/Ollama）
    │   ├── ai_client.py          # AI 客户端封装（您的版本）
    │   ├── exceptions.py         # 【新增】自定义业务异常 BizException
    │   ├── logging_config.py     # 【新增】日志配置（控制台 + 滚动文件）
    │   ├── exception_handlers.py # 【新增】全局异常处理器
    │   └── middleware.py         # 【新增】日志拦截中间件
    └── models/
        ├── __init__.py
        ├── schemas.py            # 请求/响应模型（ChatRequest, ChatResponse）
        └── response.py           # 【新增】统一 API 响应模型 APIResponse
```

# 项目启动

## 方式一：使用启动脚本
```bash
python run.py
```

## 方式二：直接运行 main.py（适合 PyCharm）
```bash
python app/main.py
```

## 方式三：使用 uvicorn 命令
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
启动成功后，服务运行在：`http://localhost:8000`

# 运行测试

## 运行全部测试（含真实 AI 调用）
```bash
pytest tests/ -v -s
```

## 只跑快速测试（跳过 integration 标记）
```bash
pytest tests/ -v -s -m "not integration"
```

# 接口文档地址

- **Swagger UI**：http://localhost:8000/docs
- **ReDoc**：http://localhost:8000/redoc
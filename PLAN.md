# 项目结构

```
fastapi-ai-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   ├── api/
│   │   ├── __init__.py
│   │   └── chat.py             # /ai/chat 路由
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # 环境变量配置
│   │   └── ai_client.py        # AI 客户端封装（支持 DeepSeek 和 Ollama）
│   └── models/
│       ├── __init__.py
│       └── schemas.py          # Pydantic 请求/响应模型
├── .env                         # 环境变量（不提交 Git）
├── .gitignore
├── requirements.txt
└── run.py                      # 启动脚本
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

# 接口文档地址

- **Swagger UI**：http://localhost:8000/docs
- **ReDoc**：http://localhost:8000/redoc
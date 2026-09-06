from fastapi import FastAPI
from app.api import chat

app = FastAPI(
    title="AI Microservice",
    version="1.0",
    description="一个简单的 AI 网关服务，集成 DeepSeek"
)

# 注册路由
app.include_router(chat.router)

# 根路由，返回服务状态
@app.get("/")
async def root():
    return {"message": "AI Service is running"}

#方便PyCharm直接运行
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

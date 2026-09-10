"""
使用pytest + requests 对FastAPI服务进行黑盒测试
运行前需先启动 FastAPI 服务（uvicorn app.main:app）。
"""
import requests
import pytest

#=======正常场景测试=======
@pytest.mark.integration # 标记为集成测试（会真实调用AI,耗时较长）
def test_chat_normal(base_url):
    """正常请求，返回AI回复"""
    # 构建请求URL
    resp = requests.post(
        f"{base_url}/ai/chat",
        json={"prompt": "用一句话介绍你自己"},
        timeout=60,
    )
    # 断言响应状态码为200
    #检查 resp.status_code == 200 这个条件是否为 True
    assert resp.status_code == 200

    #获取响应数据
    data = resp.json()
    #断言响应体
    assert "reply" in data
    assert isinstance(data["reply"], str)
    assert len(data["reply"]) > 0
    # 打印响应体
    print(f"\n[正常请求] AI 回复: {data['reply'][:80]}...")

# ============ 业务异常场景（不调用 AI，速度很快） ============

def test_chat_empty_prompt(base_url):
    """空提示，返回错误响应40001"""
    # 构建请求URL
    resp = requests.post(f"{base_url}/ai/chat",json={"prompt": ""})
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 40001
    assert data["message"] == "prompt 不能为空"
    assert data["data"] is None

def test_chat_whitespace_prompt(base_url):
    """仅包含空格的提示，返回错误响应40001"""
    resp = requests.post(
        f"{base_url}/ai/chat",
        json={"prompt": "  "},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 40001

def test_chat_contains_keyword(base_url):
    """
    prompt包含关键字error，返回错误响应40001
    error关键字模拟AI服务异常情况
    """
    resp = requests.post(
        f"{base_url}/ai/chat",
        json={"prompt": "这是一个错误的提示，包含error关键字"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 40002
    assert "error" in data["message"]

# ============ 参数校验场景（FastAPI 内置 422） ============

def test_chat_missing_keyword(base_url):
    """缺少prompt 字段，Pydantic 校验失败，返回错误响应422"""
    resp = requests.post(f"{base_url}/ai/chat")
    assert resp.status_code == 422

def test_chat_invalid_prompt(base_url):
    """非法 JSON：FastAPI 返回 422"""
    resp = requests.post(
        f"{base_url}/ai/chat",
        data="not a json",
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 422

# ============ 健康检查 ============

def test_root(base_url):
    """根路径健康检查"""
    resp = requests.get(f"{base_url}/")
    assert resp.status_code == 200
    assert resp.json()["message"] == "AI Service is running"